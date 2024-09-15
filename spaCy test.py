import tkinter as tk
import spacy
import json
import subprocess
import os

# Load spaCy model
nlp = spacy.load("en_core_web_trf")

# Define the dictionary and contextual phrases
dictionary = {
    "PlayStation 5": "PlayStation 5 is a home video game console developed by Sony Interactive Entertainment, released in 2020.",
    "Xbox Series X": "Xbox Series X is a home video game console developed by Microsoft, released in 2020.",
    # Add more definitions as needed
}

contextual_phrases = {
    "hello": "Hi there! How can I assist you today?",
    "hi": "Hello! What can I do for you?",
    "wow": "That's interesting! What else can I help you with?",
    "cool": "Nice! Do you have any other questions?",
    "no prob": "No problem! Let me know if you need anything else.",
    "no problem": "No problem! Feel free to ask more.",
    "awesome": "Awesome! How can I assist you further?",
    "amazing": "That's amazing! What else would you like to know?",
    "magnificent": "Magnificent! Is there anything else you'd like to discuss?",
}

# Function to update definitions
def update_definitions(word, definition):
    with open("definitions.json", "r") as file:
        data = json.load(file)
    
    data[word] = definition
    
    with open("definitions.json", "w") as file:
        json.dump(data, file, indent=4)

# Function to get a response from the chatbot
def get_response(user_input):
    user_input = user_input.lower().strip()
    
    # Check for contextual phrases
    for phrase, response in contextual_phrases.items():
        if phrase in user_input:
            return response

    # Check for definitions
    for word, definition in dictionary.items():
        if word.lower() in user_input:
            return f"The {word} is {definition}. Did that help?"

    # Process using spaCy
    doc = nlp(user_input)
    if len(doc.ents) > 0:
        return "Sorry, I don't know what that means."
    
    # Default response if nothing matches
    return "Sorry, I don't know what that means."

# Function to send messages and update chatlog
def send_message():
    user_input = user_input_entry.get()
    response = get_response(user_input)
    
    chatlog.config(state=tk.NORMAL)
    chatlog.insert(tk.END, f"You: {user_input}\n")
    chatlog.insert(tk.END, f"Bot: {response}\n\n")
    chatlog.config(state=tk.DISABLED)
    
    user_input_entry.delete(0, tk.END)

# Function to open update definitions script
def open_update_definitions():
    current_path = os.path.dirname(os.path.abspath(__file__))
    subprocess.Popen(["python", os.path.join(current_path, "update_definitions.py")])

# Initialize the Tkinter window
root = tk.Tk()
root.title("Not That Great GPT Version 2")

# Chatlog display (output box)
chatlog = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
chatlog.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User input field
user_input_entry = tk.Entry(root, width=40)
user_input_entry.grid(row=1, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

# Update Definitions button
update_definitions_button = tk.Button(root, text="Update Definitions", command=open_update_definitions)
update_definitions_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the Tkinter main loop
root.mainloop()
