# wrappers
from dotenv import load_dotenv
from openai import AsyncOpenAI
from ragas.llms import llm_factory
from ragas.metrics.collections import ResponseGroundedness

load_dotenv()

client = AsyncOpenAI()
llm = llm_factory("gpt-4.1-nano", client=client)
scorer = ResponseGroundedness(llm=llm)


def hitrate(expected_documents: list[str], output_documents: list[str]) -> float:
    """
    Calculate hit rate between expected and output documents for RAG evaluation.

    Hit rate measures whether the retrieval system found at least one relevant document.
    Returns 1.0 if there's any intersection between expected and retrieved documents,
    0.0 otherwise. Special case: both empty lists return 1.0 (no retrieval needed).

    Args:
        expected_documents: Ground truth documents that should be retrieved
        output_documents: Documents actually retrieved by the system

    Returns:
        1.0 if any expected document was retrieved, 0.0 otherwise
    """
    # Handle None inputs gracefully
    expected_documents = expected_documents or []
    output_documents = output_documents or []

    if not expected_documents and not output_documents:
        # print("No expected documents and no output documents")
        return 1

    return int(bool(set(expected_documents) & set(output_documents)))


# Create metric
async def aresponse_groundedness(
    response: str,
    retrieved_contexts: list[str],
    scorer: ResponseGroundedness = scorer,
) -> float:
    result = await scorer.ascore(
        response=response, retrieved_contexts=retrieved_contexts
    )
    return result.value
