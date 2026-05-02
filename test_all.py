"""
Unit Tests - Text Summarization Chatbot
Run: python test_all.py
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
