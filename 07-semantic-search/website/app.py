from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import Flask-CORS
import requests
from urllib.parse import quote
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/episode/<id>', methods=['GET'])
def index(id):
    # Encode the ID for safe URL use
    encoded_id = quote(id)
    
    # Query Solr with the encoded ID
    try:
        solr_url = f'http://localhost:8983/solr/priProj/select?q=id:"{encoded_id}"&wt=json'
        response = requests.get(solr_url)
        response.raise_for_status()  # Raise an error if the request failed
        
        # Parse the response JSON
        solr_data = response.json()
        if solr_data.get('response', {}).get('numFound', 0) == 0:
            return "Episode not found", 404
        
        # Pass the document to the template
        episode = solr_data['response']['docs'][0]
        return render_template('episode.html', id = id,episode=episode)
    
    except requests.exceptions.RequestException as e:
        # Handle request errors
        return f"Error communicating with Solr: {e}", 500

@app.route('/')
def home():
    return render_template('index.html')


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
