"""
═══════════════════════════════════════════════════════════════════════
                  UNIT TESTS  —  TEXT SUMMARIZER
═══════════════════════════════════════════════════════════════════════

WHAT THIS CODE DOES
-------------------
This file contains AUTOMATED UNIT TESTS for the three core modules of
the Text Summarizer app:

  • Summariser   → the AI engine connector
  • ChatBot      → the conversation history store
  • FileReader   → the file-loading helper

The tests run WITHOUT needing Ollama to be open — network calls are
faked using unittest.mock.patch — so they finish in seconds and prove
the code's logic works even when the AI is offline.

HOW TO RUN
----------
    python test_all.py

The output shows each test name and whether it PASSED or FAILED, plus
a summary at the bottom.


WHAT EACH TEST CLASS CHECKS
---------------------------

  ── TestSummariser ──
  Verifies the AI-connector module behaves correctly:
      • test_empty / test_whitespace
            Returns an ERROR message when no text is given.
      • test_wc_50 / test_wc_100 / test_wc_default
            The word-count extractor picks up "50", "100", or falls
            back to "75" when no number is mentioned.
      • test_fmt_bullet / test_fmt_simple / test_fmt_sentence
            The format detector picks the right style based on
            keywords in the user's instruction.
      • test_offline / test_stream_offline
            When Ollama is unreachable, the module returns a clean
            error message instead of crashing — for both normal and
            streaming modes.

  ── TestChatBot ──
  Verifies the conversation memory works correctly:
      • test_add        → a new message increases the count
      • test_clear      → clear() empties the history
      • test_last_summary → returns the most recent AI reply
      • test_empty_last → returns an empty string if no summary yet
      • test_count      → counts multiple messages correctly

  ── TestFileReader ──
  Verifies file loading works correctly:
      • test_read_txt   → reads a real .txt file from disk
      • test_missing    → returns ERROR if the file does not exist
      • test_bad_ext    → returns ERROR for unsupported types (.pdf)


KEY TECHNIQUES USED
-------------------
  • unittest          → Python's built-in testing framework
  • setUp()           → creates a fresh object before each test so
                        tests do not interfere with each other
  • patch()           → temporarily replaces ollama.chat with a fake
                        that raises an exception, letting us test the
                        offline / error path safely
  • tempfile          → creates real temporary files on disk so the
                        FileReader can be tested with actual files,
                        which are deleted afterwards with os.unlink


WHY IT MATTERS
--------------
These tests act as a SAFETY NET. If anyone changes the code later
(e.g. tweaks the Summariser prompt or adds a feature to ChatBot),
running this file instantly shows whether anything important has
broken — without having to manually click through the app.

═══════════════════════════════════════════════════════════════════════
"""


import unittest
from unittest.mock import patch
import tempfile, os

from summariser  import Summariser
from chatbot     import ChatBot
from file_reader import FileReader


class TestSummariser(unittest.TestCase):
    def setUp(self): self.s = Summariser()

    def test_empty(self):
        self.assertIn("ERROR", self.s.summarise(""))

    def test_whitespace(self):
        self.assertIn("ERROR", self.s.summarise("  "))

    def test_wc_50(self):
        self.assertEqual(self.s._wc("50 words"), "50")

    def test_wc_100(self):
        self.assertEqual(self.s._wc("100 words"), "100")

    def test_wc_default(self):
        self.assertEqual(self.s._wc("summarise"), "75")

    def test_fmt_bullet(self):
        self.assertIn("bullet", self.s._fmt("bullet points").lower())

    def test_fmt_simple(self):
        self.assertIn("simple", self.s._fmt("make it simple").lower())

    def test_fmt_sentence(self):
        self.assertIn("sentence", self.s._fmt("one sentence").lower())

    def test_offline(self):
        with patch("summariser.ollama.chat", side_effect=Exception("fail")):
            r = self.s.summarise("text")
        self.assertIn("Ollama", r)

    def test_stream_offline(self):
        tokens = []
        with patch("summariser.ollama.chat", side_effect=Exception("fail")):
            r = self.s.summarise_stream("text",
                                        on_token=lambda t: tokens.append(t))
        self.assertIn("Ollama", r)


class TestChatBot(unittest.TestCase):
    def setUp(self): self.b = ChatBot()

    def test_add(self):
        self.b.add_message("user", "hi")
        self.assertEqual(self.b.count(), 1)
P
    def test_clear(self):
        self.b.add_message("user", "hi")
        self.b.clear()
        self.assertEqual(self.b.count(), 0)

    def test_last_summary(self):
        self.b.add_message("assistant", "summary here")
        self.assertEqual(self.b.last_summary(), "summary here")

    def test_empty_last(self):
        self.assertEqual(self.b.last_summary(), "")

    def test_count(self):
        self.b.add_message("user", "a")
        self.b.add_message("assistant", "b")
        self.assertEqual(self.b.count(), 2)


class TestFileReader(unittest.TestCase):
    def setUp(self): self.r = FileReader()

    def test_read_txt(self):
        with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt",
                delete=False, encoding="utf-8") as f:
            f.write("Hello world")
            path = f.name
        try:
            self.assertEqual(self.r.read(path), "Hello world")
        finally:
            os.unlink(path)

    def test_missing(self):
        self.assertIn("ERROR", self.r.read("nope.txt"))

    def test_bad_ext(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            path = f.name
        try:
            self.assertIn("ERROR", self.r.read(path))
        finally:
            os.unlink(path)


if __name__ == "__main__":
    print("=" * 50)
    print("  Text Summarizer - Unit Tests")
    print("=" * 50)
    unittest.main(verbosity=2)
