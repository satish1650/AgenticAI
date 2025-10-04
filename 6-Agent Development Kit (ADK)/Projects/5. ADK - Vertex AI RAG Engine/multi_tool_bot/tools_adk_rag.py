import os
from dotenv import load_dotenv
import vertexai
from vertexai import rag

load_dotenv()

# Constants
PROJECT_ID = "gen-lang-client-0634579487"
LOCATION = "us-east4"
DISPLAY_NAME = "atgaga" # Corpus Display Name
PATH = [
    # TODO: Add your Actual GCG or Google Drive Path here
    "gs:/rag-data-adk/1706.03762v7.pdf"
]

def get_all_corpora() -> dict:
    """Retrieves all existing RAG corpora from Vertex AI.

    Returns:
        dict: A structured dictionary containing the list of all RAG corpora,
              or an error message if retrieval fails.
    """
    try:
        # Ensure Vertex AI is initialized
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # List all corpora
        corpora = list(rag.list_corpora())

        if not corpora:
            return {
                "status": "success",
                "message": "No RAG corpora found in the project.",
                "corpora": [],
            }

        # Build structured corpus info
        corpus_list = []
        for corpus in corpora:
            corpus_list.append({
                "name": corpus.name,
                "display_name": corpus.display_name,
                "create_time": str(corpus.create_time),
                "update_time": str(corpus.update_time),
                "description": getattr(corpus, "description", None),
            })

        return {
            "status": "success",
            "total_corpora": len(corpus_list),
            "corpora": corpus_list,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to list RAG corpora: {str(e)}",
        }