import os
import vertexai
from vertexai import rag
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-east4"

DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_TOP = 3
DEFAULT_DISTANCE_THRESHOLD = 0.5
DEFAULT_EMBEDDING_MODEL = "publishers/google/model/text-embedding-002"
DEFAULT_EMBEDDING_REQUESTS_PER_MIN = 1000

vertexai.init(project=PROJECT_ID, location=LOCATION)

print(rag.get_corpus("atgaga")) # "atgaga" corpus created in my google cloud