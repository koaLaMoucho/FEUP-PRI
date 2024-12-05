#!/usr/bin/env python3

import json
import sys
import requests

def fetch_solr_results(query_params, solr_uri, collection, output_file):
    """
    Fetch search results from a Solr instance based on the query parameters.

    Arguments:
    - query_params: Dictionary containing Solr query parameters.
    - solr_uri: URI of the Solr instance (e.g., http://localhost:8983/solr).
    - collection: Solr collection name from which results will be fetched.
    - output_file: Path to save the JSON search results.
    """
    # Construct the Solr request URL
    uri = f"{solr_uri}/{collection}/select"

    try:
        # Send the POST request to Solr
        response = requests.post(uri, json=query_params)
        response.raise_for_status()  # Raise error if the request failed
    except requests.RequestException as e:
        print(f"Error querying Solr: {e}")
        sys.exit(1)

    # Fetch results and save them to the output file
    results = response.json()
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    # Embedded JSON query
    query_params = {
        "query": "pirate ship",
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

    # Variables for Solr URI, collection, and output file
    solr_uri = "http://localhost:8983/solr"  # Solr URI
    collection = "priProj"  # Solr collection name
    output_file = "config/a_response.json"  # Output file

    # Call the function with provided variables
    fetch_solr_results(query_params, solr_uri, collection, output_file)
