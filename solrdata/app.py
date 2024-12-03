from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Enable CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model for the search query
class SolrQuery(BaseModel):
    q: str
    q_op: str = "OR"
    core: str = "priProj"

@app.post("/search")
async def search_solr(query: SolrQuery):
    """
    Endpoint to send search requests to Solr.
    """
    try:
        # Construct the Solr request URL
        solr_uri = f"http://localhost:8983/solr/{query.core}/select"
        
        # Build the query parameters
        query_params = {
            "q": query.q,
            "q.op": query.q_op,
            "wt": "json",  # Specify response format as JSON
        }

        # Send the GET request to Solr
        response = requests.get(solr_uri, params=query_params)
        response.raise_for_status()  # Raise an error if the request fails

        # Return the results as JSON
        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying Solr: {e}")
