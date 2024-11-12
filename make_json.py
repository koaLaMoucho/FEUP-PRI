import csv
import json

# Read the CSV file and process it into a list of dictionaries
def csv_to_json(csv_file, json_file):
    data_list = []  # List to hold all the episode data
    
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)  # Read CSV as dictionary
        for row in csv_reader:
            # Create a custom JSON-like structure from the CSV row
            episode_data = {
                "id": f"{row['Episode Number']}",  
                "title": row['Episode Title'],
                "air_date": row['Air Date'],
                "short_summary": row['Short Summary'],
                "long_summary": row['Long Summary'],
                "characters": row['Characters'].split(', '),  # Convert string of characters to a list
                "fruits": row['Fruits'].split(', '),  # Convert string of fruits to a list
                "rating": row['Rating']
            }
            data_list.append(episode_data)
    
    # Write the list of episodes to a JSON file
    with open(json_file, mode='w', encoding='utf-8') as jsonf:
        json.dump(data_list, jsonf, ensure_ascii=False, indent=4)

# Example usage
csv_file = 'onepiece_allepisodes_with_ratings.csv'  # Replace with your actual CSV file path
json_file = 'episodes.json'  # The output JSON file

csv_to_json(csv_file, json_file)
