import os
import pandas as pd

from qdrant_client import models

# from app.vector_store import qdrant, encoder
from app.vector_store import qdrant

from app.config import (
    COLLECTION_NAME,
    TRAIN_FILE_NAME,
    EMBEDDING_MODEL
)



# ------------------------------------------------
# Build vector database
# ------------------------------------------------

def index_data():

    # Load data
    file_path = os.path.join(
        "Input CSVs",
        TRAIN_FILE_NAME
    )

    df_train = pd.read_csv(file_path)

    print("df_train =================")
    print(df_train.head())

    # Convert dataframe into records
    data = df_train.to_dict("records")

    # Delete existing collection if present
    if qdrant.collection_exists(
        collection_name=COLLECTION_NAME
    ):
        qdrant.delete_collection(
            collection_name=COLLECTION_NAME
        )

    print("xxxxxxxxxxx Deleted existing collection xxxxxxxxxxxxx")

    # # Create collection
    # qdrant.create_collection(
    #     collection_name=COLLECTION_NAME,
    #     vectors_config=models.VectorParams(
    #         size=encoder.get_embedding_dimension(),
    #         distance=models.Distance.COSINE
    #     ),
    # )
    # Create collection
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=384,
            distance=models.Distance.COSINE
        ),
    )

    print(f"=========== QDrant Collection Created:{COLLECTION_NAME} ================")

    # # Generate embeddings and upload
    # qdrant.upload_points(
    #     collection_name=COLLECTION_NAME,
    #     points=[
    #         models.PointStruct(
    #             id=idx,
    #             vector=encoder.encode(doc["Description"]).tolist(),
    #             payload=doc
    #         )
    #         for idx, doc in enumerate(data)
    #     ]
    # )

    # Generate embeddings and upload
    qdrant.upload_points(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=idx,
                vector=models.Document(
                    text=doc["Description"],
                    model=EMBEDDING_MODEL
                ),
                payload=doc
            )
            for idx, doc in enumerate(data)
        ]
    )

    print("########### Vector store initialized successfully. ##########################")

    #Count the no of records which were uploaded to the server
    count_result = qdrant.count(
        collection_name=COLLECTION_NAME,
        exact=True
    )
    print(f"Rows in source data: {len(data)}")
    print(f"Points in Qdrant: {count_result.count}")

# ------------------------------------------------
# Run only when this file is executed directly
# ------------------------------------------------
if __name__ == "__main__":
    print("########### Starting Data Indexing ########################")
    index_data()
