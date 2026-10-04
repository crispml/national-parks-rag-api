import os
from dotenv import load_dotenv

load_dotenv()


# -------------------------
# API Keys / URLs
# -------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# QDRANT_URL="http://localhost:6333"
QDRANT_URL="https://1400f27a-86d5-4a53-9a88-553ef48d5067.us-east-1-1.aws.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


# -------------------------
# Models
# -------------------------

GEMINI_MODEL = "gemini-2.5-flash"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# -------------------------
# RAG settings
# -------------------------
TRAIN_FILE_NAME = "US National Park DB.csv"
COLLECTION_NAME = "national_parks"

TOP_K = 3