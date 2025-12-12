import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langfuse._client.client import Langfuse

this_dir = Path(__file__).parent
PATH_DATA = this_dir / "data" / "items_eval_en.json"
DATASET_NAME = "rag-eval-dataset"
DATASET_DESCRIPTION = "This is a dataset for evaluating the RAG system"
DATASET_METADATA = {"version": "1.0.0"}


def create_langfuse_client() -> Langfuse:
    load_dotenv()
    return Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_BASE_URL"],
    )


def create_dataset(
    name: str,
    description: str = None,
    metadata: dict = None,
    langfuse_client: Langfuse = None,
):

    langfuse_client.create_dataset(
        name=name,
        # optional description
        description=description,
        # optional metadata
        metadata=metadata if metadata else {},
    )
    print(f"Dataset created: {name}")


def populate_dataset(dataset_name: str, data: list, langfuse_client: Langfuse):
    for example in data:
        langfuse_client.create_dataset_item(
            dataset_name=dataset_name,
            # any python object or value, optional
            input=example["input"],
            # any python object or value, optional
            expected_output=example["expected_output"],
            metadata=example["metadata"],
            # metadata, optional
        )
    print(f"Dataset populated: {dataset_name}")


def main():
    langfuse_client = create_langfuse_client()
    # Verify connection
    if langfuse_client.auth_check():
        print("Langfuse client is authenticated and ready!")
    else:
        print("Authentication failed. Please check your credentials and host.")

    create_dataset(
        name=DATASET_NAME,
        description=DATASET_DESCRIPTION,
        metadata=DATASET_METADATA,
        langfuse_client=langfuse_client,
    )

    with open(PATH_DATA, "r") as f:
        data = json.load(f)

    populate_dataset(
        dataset_name=DATASET_NAME,
        data=data,
        langfuse_client=langfuse_client,
    )


if __name__ == "__main__":
    main()
