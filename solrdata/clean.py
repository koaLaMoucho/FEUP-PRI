import sys
import json
import re
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_input(input_string):
    """
    Removes unwanted Unicode characters and null bytes from the input string.
    """
    return re.sub(r'[^\x20-\x7E]+', '', input_string)

def get_embedding(text):
    """
    Generates embedding for the given text using SentenceTransformer.
    """
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    try:
        # Read JSON from STDIN and clean the input
        raw_input = sys.stdin.read()
        cleaned_input = clean_input(raw_input)

        # Parse the cleaned JSON
        data = json.loads(cleaned_input)

        # Update each document in the JSON data
        for document in data:
            # Extract fields if they exist, otherwise default to empty strings
            short_summary = document.get("short_summary", "")
            long_summary = document.get("long_summary", "")

            combined_text = short_summary + " " + long_summary
            document["vector"] = get_embedding(combined_text)

        # Output updated JSON to STDOUT
        json.dump(data, sys.stdout, indent=0, ensure_ascii=False)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"JSON parsing error: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An error occurred: {e}\n")
        sys.exit(1)