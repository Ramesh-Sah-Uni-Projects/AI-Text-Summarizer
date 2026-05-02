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
