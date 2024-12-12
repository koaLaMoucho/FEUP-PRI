import requests
from sentence_transformers import SentenceTransformer
import json  # To save results in JSON format

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_knn_query(endpoint, collection, embedding):
    url = f"{endpoint}/{collection}/select"
    data = {
        "q": f"{{!knn f=vector topK=40}}{embedding}",
        "fl": "id,score",
        "rows": 40,
        "wt": "json"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def display_results(results, output_file=None):
    docs = results.get("response", {}).get("docs", [])
    if not docs:
        print("No results found.")
        return
    
    output_data = []
    for doc in docs:
        result = {
            "id": doc.get("id"),
            "score": doc.get("score")
        }
        output_data.append(result)
        print(f"* {result['id']}[score: {result['score']:.2f}]")

    # Write results to file if output_file is provided
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)
        print(f"\nResults written to '{output_file}'")

def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "priProj"
    output_file = "resultsquery4.json"  # File to save results

    query_text = "Luffy loses battle"
    embedding = text_to_embedding(query_text)

    try:
        results = solr_knn_query(solr_endpoint, collection, embedding)
        display_results(results, output_file=output_file)
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()
