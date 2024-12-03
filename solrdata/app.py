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

class SolrQuery(BaseModel):
    q: str  # The query term
    q_op: str = "AND"  # Default to "OR" for logical operator
    core: str = "priProj"  # Default core name
    fields: str = "*"  # Default to retrieving all fields
    rows: int = 40  # Default number of rows returned

    # Additional parameters
    defType: str = "edismax"  # Default query parser
    q_op_default: str = "AND"  # Default operation for queries
    sort: str = "score desc"  # Sort by score in descending order
    fl: str = "* ,score"  # Return all fields and the score
    qf: str = "title^6 short_summary^3 long_summary^2 characters^1 air_date^1 fruits^1"  # Query fields with boosts
    pf: str = "title^6 short_summary^3 long_summary^2 characters^1 air_date^1 fruits^1"  # Phrase fields with boosts
    ps: int = 2  # Phrase slop
    qs: int = 2  # Query slop

    def to_solr_params(self):
        """
        Convert the SolrQuery object into the query parameters for Solr.
        """
        return {
            "q": self.q,
            "q.op": self.q_op,
            "core": self.core,
            "fl": self.fl,
            "params": {
                "defType": self.defType,
                "q.op": self.q_op_default,
                "sort": self.sort,
                "fl": self.fl,
                "qf": self.qf,
                "pf": self.pf,
                "ps": self.ps,
                "qs": self.qs,
                "rows": self.rows
            }
        }

@app.post("/search")
async def search_solr(query: SolrQuery):
    """
    Endpoint to send search requests to Solr.
    """
    try:
        # Construct the Solr request URL
        solr_uri = f"http://localhost:8983/solr/{query.core}/select"

        # Convert SolrQuery object to query parameters
        query_params = query.to_solr_params()

        # Send the GET request to Solr
        response = requests.get(solr_uri, params=query_params)
        response.raise_for_status()  # Raise an error if the request fails

        # Return the results as JSON
        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying Solr: {e}")
