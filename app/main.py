# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.retrieval import get_top_parks
from app.rag import build_context, generate_answer
# from scripts.index_data import index_data

app = FastAPI(
    title="US National Parks API",
    description="RAG-based US National Park recommendation API",
    version="2.0.0"
)


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Park recommendation question"
    )




# @app.on_event("startup")
# def startup_event():
#     index_data()


@app.get("/")
def root():
    return {
        "message": "National Parks RAG API is running"
    }

@app.post("/query")
def query_park(request: QueryRequest):

    try:
        user_query = request.query.strip()

        if not user_query:
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )

        # Retrieve relevant parks
        hits = get_top_parks(user_query)

        if not hits:
            raise HTTPException(
                status_code=400,
                detail="No relevant parks found"
            )

        # Build RAG context
        context = build_context(hits)

        # Generate answer using Gemini
        answer = generate_answer(
            user_query,
            context
        )

        return {
            "query": user_query,
            "answer": answer,
            # "context": context
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occured while processing the request : {str(e)}"
        )
