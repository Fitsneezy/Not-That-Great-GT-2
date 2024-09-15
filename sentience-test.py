import tkinter as tk
import random
import spacy
import re

# Load the spaCy model
nlp = spacy.load("en_core_web_trf")

# Definitions dictionary
dictionary = {
    "PlayStation 5": "PlayStation 5 is a home video game console developed by Sony Interactive Entertainment, released in 2020.",
    "Xbox Series X": "Xbox Series X is a home video game console developed by Microsoft, released in 2020.",
    "Windows 11": "Windows 11 is an operating system developed by Microsoft, released in 2021.",
    # Add more definitions here...
}

# Contextual phrases
contextual_phrases = {
    "hello": "Hi there! How can I assist you today?",
    "hi": "Hello! What can I do for you?",
    # Add more contextual phrases here...
}

# Conversational phrases
conversational_phrases = {
    "what's up": "Not much! Just here to help you out.",
    "how are you": "I'm just a bot, but I'm doing great! How about you?",
    # Add more conversational phrases here...
}

# Memes and humorous responses
memes = {
    "touch grass": "Sorry, I don't know what that means.",
    "ping me": "Sorry, I don't know what that means.",
    # Add more meme responses here...
}

# Helper function for whole word matching
def find_best_match(text, dictionary):
    # Normalize the text
    text = text.lower()
    for term in dictionary:
        # Use regular expressions to find whole words only
        if re.search(r'\b' + re.escape(term.lower()) + r'\b', text):
            return term
    return None

# Bot responses
def get_response(user_input):
    # Normalize the user input
    user_input = user_input.lower()
    
    # Process user input
    doc = nlp(user_input)
    response = None

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

# Function to make the bot talk whenever it wants
def self_talk():
    phrases = [
        "Did you know? The internet is full of amazing things!",
        "Here's a fun fact: The shortest war in history lasted just 38 to 45 minutes!",
        "If you need any help, feel free to ask!",
        "hello?",
        # Add more self-talking phrases here...
    ]
    return random.choice(phrases)

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

# Add self-talking capability (every 5 minutes, for example)
def periodic_talk():
    if random.random() < 0.1:  # Adjust frequency here
        chatlog.config(state=tk.NORMAL)
        chatlog.insert(tk.END, f"Bot: {self_talk()}\n")
        chatlog.config(state=tk.DISABLED)
    root.after(30000, periodic_talk)  # Check every 30 seconds

periodic_talk()  # Start

root.mainloop()
