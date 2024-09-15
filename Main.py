import tkinter as tk
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")

# Define the context manager class
class ContextManager:
    def __init__(self):
        self.context = []

    def update_context(self, text):
        self.context.append(text)
        if len(self.context) > 5:  # Keep only the last 5 messages
            self.context.pop(0)

    def get_context(self):
        return " ".join(self.context)

context_manager = ContextManager()

# Definitions dictionary
dictionary = {
    "PlayStation 5": "PlayStation 5 is a home video game console developed by Sony Interactive Entertainment, released in 2020.",
    "Xbox Series X": "Xbox Series X is a home video game console developed by Microsoft, released in 2020.",
    "Windows 11": "Windows 11 is an operating system developed by Microsoft, released in 2021.",
}

# Contextual phrases
contextual_phrases = {
    "hello": "Hi there! How can I assist you today?",
    "hi": "Hello! What can I do for you?",
}

# Conversational phrases
conversational_phrases = {
    "what's up": "Not much! Just here to help you out.",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
}

# Memes and humorous responses
memes = {
    "touch grass": "Sorry, What?.",
    "ping me": "Sorry, I'm not sure what that means.",
}

# Helper function for whole word matching
def find_best_match(text, dictionary):
    text = text.lower()
    for term in dictionary:
        if re.search(r'\b' + re.escape(term.lower()) + r'\b', text):
            return term
    return None

# Function to handle user input
def get_response(user_input):
    user_input = user_input.lower()
    doc = nlp(user_input)
    response = None

    # Update and retrieve context
    context_manager.update_context(user_input)
    context = context_manager.get_context()

    # Check for contextual phrases
    for phrase in contextual_phrases:
        if re.search(r'\b' + re.escape(phrase) + r'\b', user_input):
            response = contextual_phrases[phrase]
            break

    # Check for conversational phrases
    if response is None:
        for phrase in conversational_phrases:
            if re.search(r'\b' + re.escape(phrase) + r'\b', user_input):
                response = conversational_phrases[phrase]
                break

    # Check for definitions
    if response is None:
        best_match = find_best_match(user_input, dictionary)
        if best_match:
            response = f"The {best_match} is {dictionary[best_match]}. Did that help?"

    # Check for memes
    if response is None:
        for meme in memes:
            if re.search(r'\b' + re.escape(meme) + r'\b', user_input):
                response = memes[meme]
                break

    # Default response
    if response is None:
        response = "Sorry, I don't know what that means."

    return response

# Function to handle user input
def send_message():
    user_message = user_input_entry.get()
    bot_response = get_response(user_message)
    
    # Update chatlog
    chatlog.config(state=tk.NORMAL)
    chatlog.insert(tk.END, f"User: {user_message}\n")
    chatlog.insert(tk.END, f"Bot: {bot_response}\n")
    chatlog.config(state=tk.DISABLED)
    
    # Clear user input field
    user_input_entry.delete(0, tk.END)

# Initialize the Tkinter window
root = tk.Tk()
root.title("NTGGt Chatbot")

# Chatlog display (output box)
chatlog = tk.Text(root, state=tk.DISABLED, wrap=tk.WORD, width=50, height=20)
chatlog.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

# User input field
user_input_entry = tk.Entry(root, width=40)
user_input_entry.grid(row=1, column=0, padx=10, pady=10)

# Send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()
