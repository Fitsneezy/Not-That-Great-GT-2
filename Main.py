import tkinter as tk
from tkinter import simpledialog
import subprocess
import os
import json
import spacy
from fuzzywuzzy import process  # Import fuzzywuzzy for fuzzy matching

# Load spaCy model
nlp = spacy.load("en_core_web_trf")

# Definitions dictionary
definitions = {
    "PlayStation 5": "PlayStation 5 is a home video game console developed by Sony Interactive Entertainment, released in 2020.",
    "Xbox Series X": "Xbox Series X is a home video game console developed by Microsoft, released in 2020.",
    "Windows 11": "Windows 11 is an operating system developed by Microsoft, released in 2021.",
    "macOS Ventura": "macOS Ventura is the operating system for Apple's Mac computers, released in 2022.",
    "JavaScript": "JavaScript is a programming language used primarily for adding interactivity to web pages.",
    "HTML": "HTML stands for HyperText Markup Language and is used to create the structure of web pages.",
    "CSS": "CSS stands for Cascading Style Sheets and is used to style the appearance of web pages.",
    "Node.js": "Node.js is an open-source, cross-platform JavaScript runtime environment that executes JavaScript code outside a web browser.",
    "Express.js": "Express.js is a minimal and flexible Node.js web application framework that provides a robust set of features for building web and mobile applications.",
    "API": "API stands for Application Programming Interface. It is a set of rules and tools for building software applications, allowing different software systems to communicate with each other.",
    "JSON": "JSON stands for JavaScript Object Notation. It is a lightweight data-interchange format that is easy for humans to read and write and easy for machines to parse and generate.",
    "REST": "REST stands for Representational State Transfer. It is an architectural style for designing networked applications using stateless, client-server communication.",
    "The Legend of Zelda: Breath of the Wild": "An action-adventure game developed and published by Nintendo, released in 2017.",
    "Super Mario Odyssey": "A platform game developed and published by Nintendo, released in 2017.",
    "Minecraft": "A sandbox video game developed by Mojang Studios, originally released in 2011.",
    "Animal Crossing: New Horizons": "A life simulation video game developed and published by Nintendo, released in 2020.",
    "The Legend of Zelda: Tears of the Kingdom": "An action-adventure game developed and published by Nintendo, released on May 12, 2023.",
    "Fortnite": "Fortnite is an online video game developed by Epic Games, featuring a battle royale mode where players fight to be the last one standing.",
    "Among Us": "Among Us is an online multiplayer social deduction game developed by InnerSloth, where players work to complete tasks while impostors attempt to sabotage their efforts.",
    "Genshin Impact": "Genshin Impact is an open-world action role-playing game developed and published by miHoYo, released in 2020.",
    "Overwatch": "Overwatch is a team-based first-person shooter game developed and published by Blizzard Entertainment, featuring a diverse cast of characters.",
    "Wikipedia": "Wikipedia is a free online encyclopedia with articles written by volunteers and edited by anyone with internet access.",
    "Python": "Python is a high-level, interpreted programming language known for its readability and versatility, used in web development, data analysis, artificial intelligence, and more.",
    "Cloud Computing": "Cloud computing is the delivery of computing services—including servers, storage, databases, networking, software, and more—over the internet (the cloud).",
    "Machine Learning": "Machine learning is a branch of artificial intelligence that involves the development of algorithms that allow computers to learn from and make predictions based on data.",
    "Blockchain": "Blockchain is a decentralized digital ledger that records transactions across many computers so that the record cannot be altered retroactively.",
    "Internet of Things (IoT)": "IoT refers to the interconnected network of physical devices that collect and exchange data using embedded sensors, software, and other technologies.",
    "Virtual Reality (VR)": "Virtual Reality is a simulated experience that can be similar to or completely different from the real world, often experienced through VR headsets.",
    "Augmented Reality (AR)": "Augmented Reality overlays digital information on the real world, often viewed through devices like smartphones or AR glasses.",
    "Cybersecurity": "Cybersecurity involves the protection of computer systems and networks from digital attacks, theft, and damage.",
}

# Contextual phrases
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

def process_input(user_input):
    user_input_lower = user_input.lower()
    
    # Check for contextual phrases
    for phrase, response in contextual_phrases.items():
        if phrase in user_input_lower:
            return response

    # Fuzzy match for definitions
    term, score = process.extractOne(user_input, definitions.keys())
    if score > 80:  # Threshold for fuzzy matching
        definition = definitions[term]
        return f"The {term} is {definition}. Did that help?"

    return "Sorry, I don't know what that means."

def send_message():
    user_input = input_entry.get()
    response = process_input(user_input)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"User: {user_input}\nBot: {response}\n\n")
    output_text.config(state=tk.DISABLED)

def open_definitions_updater():
    word = simpledialog.askstring("Input", "Enter the word:")
    definition = simpledialog.askstring("Input", "Enter the definition:")
    if word and definition:
        # Update the definitions dictionary
        global definitions
        definitions[word] = definition
        
        # Save definitions to a file
        with open('definitions.txt', 'a') as file:
            file.write(f"{word}:{definition}\n")
        
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"Definition for '{word}' updated.\n\n")
        output_text.config(state=tk.DISABLED)

def create_settings_menu():
    settings_menu = tk.Toplevel()
    settings_menu.title("Settings Menu")

    update_button = tk.Button(settings_menu, text="Update Definitions", command=open_definitions_updater)
    update_button.pack(pady=20)

# Main UI
root = tk.Tk()
root.title("AI Chatbot")

input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

output_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, height=15, width=50)
output_text.pack(pady=10)

settings_button = tk.Button(root, text="Settings", command=create_settings_menu)
settings_button.pack(pady=10)

root.mainloop()
