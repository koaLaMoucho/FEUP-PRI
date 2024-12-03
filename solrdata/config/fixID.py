import sys

def process_text(input_text):
    lines = input_text.strip().splitlines()
    processed_lines = []

    for line in lines:
        # Remove the space after "Episode" by replacing "Episode " with "Episode"
        processed_line = line.replace("Episode ", "Episode")
        processed_lines.append(processed_line)
    
    # Join the processed lines back into a single string and return
    return "\n".join(processed_lines)

if __name__ == "__main__":
    # Read all input from stdin
    input_text = sys.stdin.read()
    
    # Process the text
    result = process_text(input_text)
    
    # Print the result to standard output
    print(result)