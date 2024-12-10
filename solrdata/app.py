from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
import requests

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)



@app.route('/fetch_documents', methods=['POST'])
def fetch_documents():
    """
    API endpoint to fetch Solr documents.
    Expects JSON payload with 'query' parameter.
    """
    try:
        data = request.json
        query = data.get("query", "*:*")  # Default to match all if no query
        solr_uri = "http://localhost:8983/solr"  # Solr URI
        collection = "priProj"  # Solr collection name

        # Query parameters for Solr
        query_params = {
            "query": query,
            "fields": "*,score",
            "params": {
                "defType": "edismax",
                "q.op": "AND",
                "sort": "score desc",
                "fl": "*,score",
                "qf": "title^6 short_summary^3 long_summary^2 characters^1 air_date^1 fruits^1",
                "pf": "title^6 short_summary^3 long_summary^2 characters^1 air_date^1 fruits^1",
                "ps": 2,
                "qs": 2,
                "rows": 40
            }
        }

        # Construct Solr request URL
        uri = f"{solr_uri}/{collection}/select"

        # Fetch results from Solr
        response = requests.post(uri, json=query_params)
        response.raise_for_status()

        # Return Solr response
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Error querying Solr: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
