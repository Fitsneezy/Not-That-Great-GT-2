import sys
import json
import os

def update_definitions(word, definition):
    # Path to the definitions file
    definitions_file = 'definitions.json'

    if os.path.exists(definitions_file):
        with open(definitions_file, 'r') as file:
            definitions = json.load(file)
    else:
        definitions = {}

    # Update the definitions dictionary
    definitions[word] = definition

    # Write back to the file
    with open(definitions_file, 'w') as file:
        json.dump(definitions, file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_definitions.py <word> <definition>")
        sys.exit(1)

    word = sys.argv[1]
    definition = sys.argv[2]

    update_definitions(word, definition)
    print(f"Definition for '{word}' updated.")
