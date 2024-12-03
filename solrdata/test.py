#!/usr/bin/env python3

import json
import sys
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Solr URI and Collection
SOLR_URI = "http://localhost:8983/solr"
COLLECTION = "priProj"  # Change this to your actual Solr collection name


@app.route('/search', methods=['POST'])
def search_solr():
    try:
        query_data = request.json  # Get the JSON data sent by the frontend
        query = query_data.get('q', '*:*')  # Default query is all documents if not provided

        # Solr query parameters
        params = {
            'q': query,
            'wt': 'json',  # Ensure Solr returns results in JSON format
            'start': 0,    # Start from the first result (can be modified based on pagination)
            'rows': 10,    # Number of results to return (can be modified)
        }

        # Send request to Solr
        response = requests.get(f"{SOLR_URI}/{COLLECTION}/select", params=params)

        if response.status_code == 200:
            return jsonify(response.json())  # Return Solr results as JSON
        else:
            return jsonify({"error": "Error querying Solr", "status": response.status_code})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
