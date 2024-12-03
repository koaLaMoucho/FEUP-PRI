import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    # Read JSON from STDIN
    data = json.load(sys.stdin)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        short_summary = document.get("short_summary", "")
        long_summary = document.get("long_summary", "")

        combined_text = short_summary + " " + long_summary
        document["vector"] = get_embedding(combined_text)

    # Output updated JSON to STDOUT
    json.dump(data, sys.stdout, ensure_ascii=True)
