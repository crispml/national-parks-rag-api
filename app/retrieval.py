# app/retrieval.py

# from app.vector_store import qdrant, encoder
from app.vector_store import qdrant

from app.config import COLLECTION_NAME, TOP_K, EMBEDDING_MODEL
from qdrant_client.models import Document


def get_top_parks(query, top_k=TOP_K):
    # # Convert natural-language query into embedding
    # query_vector = encoder.encode(query).tolist()

    # # Search Qdrant
    # response = qdrant.query_points(
    #     collection_name=COLLECTION_NAME,
    #     query=query_vector,
    #     limit=top_k
    # )

    response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=Document(
            text=query,
            model=EMBEDDING_MODEL
        ),
        limit=TOP_K,
        with_payload=True
    )

    hits = response.points

    # Debugging
    print(
        "############ Qdrant Search Results ############"
    )

    for hit in hits:
        print(
            f"ID: {hit.id}, Score: {hit.score}"
        )
        print(
            f"Park Details: {hit.payload}\n"
        )

    return hits

