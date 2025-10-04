import os
from dotenv import load_dotenv
import vertexai
from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool

# Constants
PROJECT_ID = "gen-lang-client-0634579487"
LOCATION = "us-east4"
DISPLAY_NAME = "atgaga" # Corpus Display Name
PATH = [
    # TODO: Add your Actual GCG or Google Drive Path here
    "gs:/rag-data-adk/1706.03762v7.pdf"
]

# Initialize Vertex AI 
vertexai.init(project=PROJECT_ID, location=LOCATION)


# =========================================================
# 🔹 Function: Create or Get an Existing RAG Corpus
# =========================================================
def create_or_get_corpus(name: str):
    """Creates a new RAG corpus if not found, else reuses the existing one."""
    existing_corpora = list(rag.list_corpora())
    for corpus in existing_corpora:
        if corpus.display_name == name:
            print(f"🔁 Reusing existing RAG corpus: {corpus.name}")
            return corpus

    print(f"🆕 Creating new RAG corpus: {name}")
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-005"
        )
    )

    new_corpus = rag.create_corpus(
        display_name=name,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    print(f"✅ Created new RAG corpus: {new_corpus.name}")
    return new_corpus


# =========================================================
# 🔹 Main Execution
# =========================================================
def main():
    # Load environment variables
    load_dotenv()

    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us-east4"
    NAME = "atgaga"

    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # === Create or Get RAG Corpus ===
    rag_corpus = create_or_get_corpus(NAME)

    # === Import Files (only if empty) ===
    rag_files = list(rag.list_files(rag_corpus.name))
    if not rag_files:
        print("📁 Importing new files into RAG corpus...")
        paths = [
            "gs://your_bucket/sample.pdf",  # Replace with your file path
        ]
        rag.import_files(
            rag_corpus.name,
            paths,
            transformation_config=rag.TransformationConfig(
                chunking_config=rag.ChunkingConfig(
                    chunk_size=512,
                    chunk_overlap=100,
                ),
            ),
            max_embedding_requests_per_min=1000,
        )
        print("✅ Files imported successfully.")
    else:
        print(f"📚 Corpus already contains {len(rag_files)} files — skipping import.")

    # === Retrieval Configuration ===
    rag_retrieval_config = rag.RagRetrievalConfig(
        top_k=3,
        filter=rag.Filter(vector_distance_threshold=0.5),
    )

    # === Direct Context Retrieval ===
    retrieval_response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=rag_corpus.name,
            )
        ],
        text="What is RAG and why it is helpful?",
        rag_retrieval_config=rag_retrieval_config,
    )

    print("\n🔍 Direct Retrieval Response:")
    print(retrieval_response)

    # === Create a Retrieval Tool for Gemini ===
    rag_retrieval_tool = Tool.from_retrieval(
        retrieval=rag.Retrieval(
            source=rag.VertexRagStore(
                rag_resources=[
                    rag.RagResource(
                        rag_corpus=rag_corpus.name,
                    )
                ],
                rag_retrieval_config=rag_retrieval_config,
            ),
        )
    )

    # === Initialize Gemini Model ===
    rag_model = GenerativeModel(
        model_name="gemini-2.0-flash-001",
        tools=[rag_retrieval_tool],
    )

    # === Generate RAG-Augmented Response ===
    gen_response = rag_model.generate_content("What is RAG and why it is helpful?")
    print("\n🧠 Generated Response from Gemini + RAG:")
    print(gen_response.text)


# =========================================================
# 🔹 Entry Point
# =========================================================
if __name__ == "__main__":
    main()
