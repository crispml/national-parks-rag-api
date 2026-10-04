# Import tools for replacing real functions with fake/mock functions during testing.
#
# patch:
# Temporarily replaces a real function such as get_top_parks()
# with a mock version.
#
# MagicMock:
# Creates a fake Python object that can stand in for something
# like a Qdrant search result.
from unittest.mock import patch, MagicMock


# TestClient allows us to call our FastAPI endpoints from Python tests
# without actually starting Uvicorn.
from fastapi.testclient import TestClient


# Import our actual FastAPI application object from app/main.py.
#
# In main.py we have something like:
#
#     app = FastAPI()
#
from app.main import app


# Create a test client connected to our FastAPI application.
#
# This allows us to do:
#     client.get("/")
#     client.post("/query", ...)
#
# instead of opening http://localhost:8000 in a browser.
client = TestClient(app)


# ============================================================
# TEST 1: Test the root endpoint GET /
# ============================================================

def test_root():

    # Simulate someone making:
    #
    # GET /
    #
    # Equivalent to accessing the root endpoint of our API.
    response = client.get("/")

    # Check that FastAPI returned HTTP 200 (Success).
    assert response.status_code == 200

    # Check that the JSON response contains exactly the
    # message we expect.
    #
    # Expected response:
    #
    # {
    #     "message": "National Parks RAG API is running"
    # }
    assert response.json()["message"] == "National Parks RAG API is running"


# ============================================================
# TEST 2: Test FastAPI/Pydantic input validation
# ============================================================

def test_query_validation():

    # Send a POST request to /query.
    #
    # We deliberately send an invalid query:
    #
    #     "a"
    #
    # Our QueryRequest model requires a minimum query length,
    # for example:
    #
    # query: str = Field(..., min_length=3)
    response = client.post(
        "/query",
        json={"query": "a"}
    )

    # FastAPI should reject the request before our RAG pipeline runs.
    #
    # HTTP 422 = Unprocessable Content
    #
    # In this case it means the JSON structure is understood,
    # but it fails our validation rules.
    assert response.status_code == 422


# ============================================================
# TEST 3: Test the complete /query FastAPI flow
#
# BUT:
# We do NOT want to actually call:
#
#     Qdrant Cloud
#     Gemini
#
# during a unit/API test.
#
# Therefore we temporarily replace those functions with mocks.
# ============================================================


# Replace generate_answer() inside app.main with a mock.
@patch("app.main.generate_answer")

# Replace build_context() inside app.main with a mock.
@patch("app.main.build_context")

# Replace get_top_parks() inside app.main with a mock.
@patch("app.main.get_top_parks")

def test_query(
    mock_get_top_parks,
    mock_build_context,
    mock_generate_answer
):

    # --------------------------------------------------------
    # FAKE QDRANT RESPONSE
    # --------------------------------------------------------

    # Normally get_top_parks() would contact Qdrant Cloud:
    #
    # query
    #   ↓
    # Qdrant
    #   ↓
    # matching National Parks
    #
    # During this test we don't contact Qdrant.
    #
    # Instead, tell our fake get_top_parks():
    #
    # "Whenever you're called, pretend you found one result."
    mock_get_top_parks.return_value = [
        MagicMock()
    ]


    # --------------------------------------------------------
    # FAKE CONTEXT
    # --------------------------------------------------------

    # Normally build_context() would take the Qdrant results
    # and construct context for Gemini.
    #
    # Instead, force it to return this fixed text.
    mock_build_context.return_value = "Mock Park Context"


    # --------------------------------------------------------
    # FAKE GEMINI RESPONSE
    # --------------------------------------------------------

    # Normally generate_answer() would send the query + context
    # to Gemini.
    #
    # Instead, tell the mock to return this fixed answer.
    mock_generate_answer.return_value = "This Park is a good match."


    # --------------------------------------------------------
    # CALL THE REAL FASTAPI /query ENDPOINT
    # --------------------------------------------------------

    # This part is real.
    #
    # We're sending an actual test HTTP request through FastAPI.
    response = client.post(
        "/query",
        json={
            "query": "Suggest a Park with forests"
        }
    )


    # --------------------------------------------------------
    # CHECK HTTP RESPONSE
    # --------------------------------------------------------

    # The endpoint should successfully complete.
    assert response.status_code == 200


    # Convert the JSON response into a Python dictionary.
    data = response.json()


    # --------------------------------------------------------
    # CHECK THE RESPONSE CONTENT
    # --------------------------------------------------------

    # Make sure FastAPI returns the same query.
    assert data["query"] == "Suggest a Park with forests"

    # Since Gemini was mocked, we know exactly what answer
    # should be returned.
    assert data["answer"] == "This Park is a good match."


    # --------------------------------------------------------
    # CHECK THAT THE RAG PIPELINE WAS ACTUALLY EXECUTED
    # --------------------------------------------------------

    # Verify get_top_parks() was called exactly once.
    mock_get_top_parks.assert_called_once()

    # Verify build_context() was called exactly once.
    mock_build_context.assert_called_once()

    # Verify generate_answer() was called exactly once.
    mock_generate_answer.assert_called_once()