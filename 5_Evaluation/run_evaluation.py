import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from time import time
from uuid import uuid4

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from langfuse import Langfuse, observe
from qdrant_client import QdrantClient
from tqdm import tqdm
from utils.metrics import aresponse_groundedness, hitrate

sys.path.insert(0, str(Path(__file__).parent))

# Initialize the LLM
DATASET_NAME = "rag-eval-dataset"
MODEL_NAME = "gpt-5-nano"
REASONING_EFFORT = "minimal"  # could be   "minimal" | "low" | "medium" | "high"  see [https://platform.openai.com/docs/guides/latest-model]
TEMPERATURE = 0
K_RETRIEVAL = 4

PROMPT_TEMPLATE = """You are a helpful assistant answering questions about customer care for AI-Bay.

Use the following context documents to answer the user's question. If the answer is not in the provided documents, say "I don't have that information in the provided documents."

Context Documents:
{context}

User Question: {question}

Instructions:
1. Answer based ONLY on the provided documents
2. Be specific and cite which document(s) you used
3. If information is unclear or missing, say so
4. Keep answers concise but complete
5. Use a friendly, informative tone
Answer:"""


def create_langfuse_client() -> Langfuse:
    load_dotenv()
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_BASE_URL"],
    )


def load_vector_store():
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
    load_dotenv()

    this_dir = Path(__file__).parent
    path_to_vector_store = this_dir / "vector_store"

    print(f"Path to vector store: {path_to_vector_store}")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
    )

    # Remove the lock file if it exists so that we won't have the error: "The collection is already in use"
    os.remove(path_to_vector_store / ".lock")

    client = QdrantClient(path=path_to_vector_store)
    return QdrantVectorStore(
        client=client,
        collection_name="faq_collection",
        embedding=embeddings,
        sparse_embedding=sparse_embeddings,
        vector_name="dense",
        sparse_vector_name="sparse",
        retrieval_mode=RetrievalMode.HYBRID,
    )


def format_docs_alternative(docs: list[Document]):
    """
    Format retrieved documents for inclusion in prompt

    Args:
        docs: List of Document objects

    Returns:
        Formatted string with numbered documents
    """
    formatted = []

    for i, doc in enumerate(docs, 1):
        formatted.append(
            f"Document {i}:\n{doc.metadata['faq_body']}\nSource: {doc.metadata['faq_id']}"
        )

    return "\n\n".join(formatted)


class RagConversation:
    def __init__(self, vector_store, llm, history=None):
        self.vector_store = vector_store
        self.llm = llm
        self.history = history if history else []

    def add_message(self, message: BaseMessage):
        self.history.append(message)

    @observe(name="retriever-call", as_type="retriever")
    def retrieve_documents(self, question, K=K_RETRIEVAL):
        docs_and_scores = self.vector_store.similarity_search_with_relevance_scores(
            question, k=K
        )
        return docs_and_scores

    @observe(name="llm-call", as_type="generation")
    def generate_response(self, question, docs):
        context_str = format_docs_alternative(docs)
        prompt = PROMPT_TEMPLATE.format(context=context_str, question=question)
        response = self.llm.invoke(prompt)
        return response.content

    @observe
    def get_response(self, question):
        docs_and_scores = self.retrieve_documents(question, K=K_RETRIEVAL)

        docs = [doc for doc, score in docs_and_scores]
        scores = [score for doc, score in docs_and_scores]

        response = self.generate_response(question, docs)
        return response, docs, scores


async def async_run_evaluation(
    dataset_name: str = DATASET_NAME,
    rag_conversation: RagConversation = None,
    langfuse_client: Langfuse = None,
):
    """
    Run evaluation for a given agent and dataset
    """

    timestamp = datetime.now().strftime("%Y-%m-%d")
    run_name = f"{timestamp}-{str(uuid4())[:4]}-{MODEL_NAME}"
    run_description = f"Run evaluation for {MODEL_NAME}"

    # Load the dataset
    dataset = langfuse_client.get_dataset(name=dataset_name)
    # Loop over the dataset items
    start_time = time()
    for item in tqdm(dataset.items):
        # Use the item.run() context manager for automatic trace linking
        with item.run(
            run_name=run_name,
            run_description=run_description,
            run_metadata={
                "model": MODEL_NAME,
                "temperature": TEMPERATURE,
                "reasoning_effort": REASONING_EFFORT,
                "k_retrieval": K_RETRIEVAL,
            },
        ) as root_span:
            # Execute your LLM-app against the dataset item input
            expected_source_ids = item.metadata["faq_ids"]
            response, retrieved_docs, similarity_scores = rag_conversation.get_response(
                item.input
            )
            retrieved_sources_ids = [doc.metadata["faq_id"] for doc in retrieved_docs]
            retrieved_contexts = [doc.page_content for doc in retrieved_docs]

            # Retrieval Score
            hitrate_score = hitrate(expected_source_ids, retrieved_sources_ids)
            root_span.score_trace(
                name="hitrate",
                value=hitrate_score,
                comment=f"expected_source_ids: {json.dumps(expected_source_ids, indent=2)}"
                f"\n\n received sources: {json.dumps(retrieved_sources_ids, indent=2)}",
            )

            # LLM Generation Score
            response_groundedness_score = await aresponse_groundedness(
                response, retrieved_contexts
            )
            root_span.score_trace(
                name="response_groundedness",
                value=response_groundedness_score,
                comment=f"response: {response}"
                f"\n\n retrieved_contexts: {json.dumps(retrieved_contexts, indent=2)}",
            )

            # Workaround to update the trace with the input and output
            langfuse_client.update_current_trace(
                input=item.input,
                output=response,
                metadata={
                    "temperature": TEMPERATURE,
                    "reasoning_effort": REASONING_EFFORT,
                    "k_retrieval": K_RETRIEVAL,
                    "scores": similarity_scores,
                    "retrieved_docs": [
                        {**doc.metadata, "content": doc.page_content}
                        for doc in retrieved_docs
                    ],
                    "expected_source_ids": expected_source_ids,
                    "expected_output": item.expected_output,
                },
                # optional, useful to add reasoning
            )

    # Flush the langfuse client to ensure all data is sent to the server at the end of the experiment run
    langfuse_client.flush()
    end_time = time()
    # logger.info(f"Evaluation time: {end_time - start_time} seconds")
    print(f"Evaluation time: {(end_time - start_time):.2f} seconds")


if __name__ == "__main__":
    load_dotenv()
    vector_store = load_vector_store()
    llm = ChatOpenAI(
        model=MODEL_NAME, temperature=TEMPERATURE, reasoning_effort=REASONING_EFFORT
    )
    rag_conversation = RagConversation(vector_store, llm)
    langfuse_client = create_langfuse_client()
    asyncio.run(
        async_run_evaluation(
            dataset_name=DATASET_NAME,
            rag_conversation=rag_conversation,
            langfuse_client=langfuse_client,
        )
    )
