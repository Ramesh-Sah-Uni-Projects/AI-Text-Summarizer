"""
═══════════════════════════════════════════════════════════════════════
                      CHATBOT  —  CONVERSATION MEMORY
═══════════════════════════════════════════════════════════════════════

WHAT THIS CODE DOES
-------------------
This class stores the conversation history between the user and the AI
for the current session. It acts as the app's short-term memory — every
piece of text the user submits and every summary the AI generates is
saved here in order.

HOW IT WORKS
------------
The history is kept as a simple list of dictionaries, where each entry
has a ROLE ("user" or "assistant") and the CONTENT of the message.

METHODS PROVIDED
----------------
  • __init__()         → creates an empty history list when the app starts
  • add_message()      → adds a new message (user input or AI reply)
  • get_history()      → returns the full conversation so far
  • clear()            → wipes the history (e.g. to start a fresh session)
  • last_summary()     → finds and returns the most recent AI summary
  • count()            → returns how many messages are stored in total
                         (used by the UI to show the session counter,
                         e.g. "3 summaries this session")

WHY IT MATTERS
--------------
Without this class, the app would forget everything after each summary.
By storing the history, the app can:
  • Track how many summaries the user has made
  • Retrieve the last summary for follow-up edits
  • Support future features like exporting the full chat log

═══════════════════════════════════════════════════════════════════════
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


 
