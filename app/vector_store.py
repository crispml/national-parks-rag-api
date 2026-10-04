# import os
# import pandas as pd

from qdrant_client import models, QdrantClient
# from sentence_transformers import SentenceTransformer

from app.config import QDRANT_URL, EMBEDDING_MODEL, QDRANT_API_KEY



# ------------------------------------------------
# Initialize Qdrant
# ------------------------------------------------
qdrant = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    cloud_inference=True,
    timeout=60
)

# # Qdrant runs in memory inside Python
# qdrant = QdrantClient(":memory:")

# # ------------------------------------------------
# # Initialize embedding model
# # ------------------------------------------------
# encoder = SentenceTransformer(
#     EMBEDDING_MODEL
# )

