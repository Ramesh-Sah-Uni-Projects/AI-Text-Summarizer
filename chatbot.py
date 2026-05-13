"""
AI Text Summarizer Chatbot
==========================

This module defines the `ChatBot` class for the NLP mini-project.

The class inherits from `ChatbotBase` (defined in `chatbot_base.py`, the
assignment template) and overrides every core method of the base class
so the chatbot can:

  - greet and say goodbye to the user
  - read user input from the terminal
  - process input into a structured action
  - generate a response by calling the local phi3:mini model via Ollama
  - run a full conversation loop until the user types 'quit'

Used by both `run_chatbot.py` (terminal entry point) and `app.py` (GUI).
"""

from chatbot_base import ChatbotBase
from summariser   import Summariser
from file_reader  import FileReader


class ChatBot(ChatbotBase):
    """
    AI-powered text-summarisation chatbot.

    Inherits from ChatbotBase (assignment template) and adds:
      - conversation history management
      - text summarisation via the local phi3:mini model (Ollama)
      - file reading for .txt / .docx
      - word-count and format instructions (bullets, simpler, one
        sentence, academic, etc.)
    """

    HELP = (
        "Commands:\n"
        "  paste            — Enter or paste text to summarize\n"
        "  50 / 75 / 100    — Set summary word count\n"
        "  bullet points    — Format as bullet points\n"
        "  simpler          — Use simpler language\n"
        "  one sentence     — Condense to one sentence\n"
        "  academic         — Use formal academic language\n"
        "  clear            — Clear current text and history\n"
        "  history          — Show conversation history\n"
        "  quit             — Exit the chatbot"
    )

    # ── Constructor ───────────────────────────────────────────────
    def __init__(self, name="AI Text Summarizer"):
        # Call the parent constructor as expected for proper inheritance.
        super().__init__(name=name)

        # The base class template sets `self.conversation_is_active = True`
        # as an INSTANCE ATTRIBUTE, which shadows the method of the same
        # name defined on the class. We want the method (overridden below)
        # to be callable, so we remove the shadowing attribute and use a
        # private flag (`self._active`) for the internal state instead.
        del self.conversation_is_active
        self._active = True

        # Conversation history for the session
        self.history = []

        # Helper modules
        self.summariser  = Summariser()
        self.file_reader = FileReader()

        # Current text loaded for summarisation
        self._current_text = ""

    # ── Overridden base class methods ─────────────────────────────

    def greeting(self):
        """Print a welcome message when the chatbot starts."""
        print("=" * 54)
        print("   AI Text Summarizer — NLP Chatbot")
        print("   Powered by phi3:mini via Ollama (fully offline)")
        print("=" * 54)
        print(f"\nHello! I am {self.name}.")
        print("I can summarize large amounts of text for you.\n")
        print(self.HELP)
        print("-" * 54)

    def farewell(self):
        """Print a goodbye message when the chatbot exits."""
        count = self.count() // 2
        print("-" * 54)
        if count:
            print(f"Session complete — {count} "
                  f"{'summary' if count == 1 else 'summaries'} generated.")
        print("Thank you for using AI Text Summarizer. Goodbye!")
        print("=" * 54)

    def conversation_is_active(self):
        """Return True while the conversation is running."""
        return self._active

    def receive_input(self):
        """Prompt the user and return their typed input."""
        try:
            return input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            return "quit"

    def process_input(self, user_input):
        """
        Analyse the user's input and return a dict describing the action.

        Returns:
            dict with keys:
                action      — "quit" | "paste" | "summarise" |
                              "clear" | "history" | "help" | "unknown"
                instruction — the raw instruction string (for summarise)
                text        — current loaded text (for summarise)
        """
        low = user_input.lower().strip()

        if not low:
            return {"action": "unknown", "text": ""}

        # Exit commands
        if low in ("quit", "exit", "bye", "q"):
            self._active = False
            return {"action": "quit"}

        # Paste / load text
        if low in ("paste", "text", "enter", "load", "input"):
            return {"action": "paste"}

        # Utility commands
        if low == "clear":
            return {"action": "clear"}

        if low in ("history", "hist"):
            return {"action": "history"}

        if low in ("help", "?", "commands"):
            return {"action": "help"}

        # Everything else → treat as a summarisation instruction
        return {
            "action":      "summarise",
            "instruction": user_input,
            "text":        self._current_text,
        }

    def generate_response(self, processed_input):
        """
        Execute the action from process_input and return a response string.

        For summarisation, the response streams directly to the terminal
        token by token and returns "" (already printed — avoids
        double-printing). For all other actions, returns a plain string
        to be printed by respond().
        """
        action = processed_input.get("action")

        # ── Quit ──────────────────────────────────────────────────
        if action == "quit":
            return None

        # ── Paste text ────────────────────────────────────────────
        if action == "paste":
            print("\nPaste your text below.")
            print("Press Enter twice when finished:\n")
            lines = []
            while True:
                try:
                    line = input()
                except (EOFError, KeyboardInterrupt):
                    break
                # Two consecutive blank lines = end of input
                if line == "" and lines and lines[-1] == "":
                    break
                lines.append(line)

            text = "\n".join(lines).rstrip()

            if not text.strip():
                return "No text entered. Type 'paste' to try again."

            self._current_text = text
            wc = len(text.split())
            return (
                f"Text loaded — {wc} words.\n"
                f"Now type an instruction, e.g. '75 words', "
                f"'bullet points', 'simpler'."
            )

        # ── Summarise ─────────────────────────────────────────────
        if action == "summarise":
            if not self._current_text:
                return (
                    "No text loaded yet.\n"
                    "Type 'paste' to enter text first."
                )

            instruction = processed_input.get("instruction", "75 words")
            print(f"\nBot: ", end="", flush=True)

            tokens = []

            def on_token(t):
                print(t, end="", flush=True)
                tokens.append(t)

            result = self.summariser.summarise_stream(
                self._current_text,
                instruction,
                on_token=on_token,
            )
            print()  # newline after streaming ends

            # Save to history
            self.add_message("user",      instruction)
            self.add_message("assistant", result)

            # Already printed via streaming — return "" so respond()
            # doesn't print it again.
            return ""

        # ── Clear ─────────────────────────────────────────────────
        if action == "clear":
            self.clear()
            return "Cleared. Text and history have been reset."

        # ── History ───────────────────────────────────────────────
        if action == "history":
            if not self.history:
                return "No history yet."
            lines = []
            for i, msg in enumerate(self.history, 1):
                role = "You" if msg["role"] == "user" else "Bot"
                snippet = msg["content"][:80].replace("\n", " ")
                lines.append(f"  {i}. [{role}] {snippet}...")
            return "Conversation history:\n" + "\n".join(lines)

        # ── Help ──────────────────────────────────────────────────
        if action == "help":
            return self.HELP

        # ── Unknown ───────────────────────────────────────────────
        return (
            "I didn't understand that.\n"
            "Type 'paste' to enter text, an instruction to summarize, "
            "or 'help' for commands."
        )

    def respond(self, out_message=None):
        """
        One full turn of the conversation:
          1. Print the previous response (if any and non-empty).
          2. Get user input.
          3. Process it.
          4. Generate and return the response.
        """
        if out_message and isinstance(out_message, str):
            print(f"\nBot: {out_message}")

        user_input = self.receive_input()
        processed  = self.process_input(user_input)
        response   = self.generate_response(processed)
        return response

    # ── History helpers (used by GUI app.py) ──────────────────────

    def add_message(self, role: str, content: str):
        """Append a message to the conversation history."""
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list:
        """Return the full conversation history."""
        return self.history

    def clear(self):
        """Clear conversation history and loaded text."""
        self.history = []
        self._current_text = ""

    def last_summary(self) -> str:
        """Return the most recent assistant response."""
        for msg in reversed(self.history):
            if msg["role"] == "assistant":
                return msg["content"]
        return ""

    def count(self) -> int:
        """Return total number of messages in history."""
        return len(self.history)
