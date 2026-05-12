"""
This ChatBot class is a simple memory store that keeps track of the conversation between the user and the AI during a session. Think of it as a notebook that records every message exchanged.

What each method does:
__init__ — Creates an empty list called history when the chatbot starts. This is where all messages will be stored.
add_message(role, content) — Adds a new message to the history. The role is either "user" or "assistant" (the AI), and content is the actual text of the message.
get_history() — Returns the full list of all messages exchanged so far. Useful if you want to send the whole conversation back to the AI for context.
clear() — Wipes the history clean. Used when the user wants to start a fresh session.
last_summary() — Looks backwards through the history to find the most recent AI response and returns it. Handy for grabbing the latest summary without scrolling through everything.
count() — Returns how many messages are stored in total. The UI uses this (divided by 2) to show "X summaries this session" in the header.
"""

class ChatBot:
    """Stores conversation history for the session."""

    def __init__(self):
        self.history = []

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list:
        return self.history

    def clear(self):
        self.history = []

    def last_summary(self) -> str:
        for msg in reversed(self.history):
            if msg["role"] == "assistant":
                return msg["content"]
        return ""

    def count(self) -> int:
        return len(self.history)


 
