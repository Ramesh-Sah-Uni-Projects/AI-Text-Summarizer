"""
═══════════════════════════════════════════════════════════════════════
                      FILE READER  —  HELPER MODULE
═══════════════════════════════════════════════════════════════════════

WHAT THIS CODE DOES
-------------------
This FileReader class is a FILE-LOADING HELPER that extracts plain text
from documents the user uploads. It supports two common formats:
  • .txt   (plain text)
  • .docx  (Microsoft Word)

It returns the content as a single string the app can feed into the AI.


IMPORTS USED
------------
  • Path from pathlib   → A modern way to handle file paths that works
                          on Windows, Mac, and Linux.
  • Document from docx  → A library (python-docx) that opens Word
                          documents and reads their content.


WHAT EACH METHOD DOES
---------------------
  • read(filepath)
        The main entry point. Checks if the file exists, looks at the
        file extension, and routes the work to the correct helper
        method. If the file is missing or the format isn't supported,
        it returns a clear "ERROR:" message instead of crashing.

  • _txt(path)
        Reads a plain .txt file. First tries UTF-8 encoding (the modern
        standard), and if that fails, falls back to latin-1 so older
        files still work. Any other error is caught and returned as a
        friendly error string.

  • _docx(path)
        Opens a Word document, loops through every paragraph, skips
        empty ones, and joins the rest together with blank lines
        between them. This preserves the document's structure while
        stripping out Word's complex formatting.


NOTE ON THE UNDERSCORE PREFIX
-----------------------------
The underscore in _txt and _docx is a Python convention meaning these
are PRIVATE HELPERS — only the read() method should call them, not
outside code.


SUMMARY
-------
This class takes the messy job of opening different file types and
turns it into one simple call:

        reader.read("myfile.docx")

which always returns either the text inside or a clean error message.

═══════════════════════════════════════════════════════════════════════
"""


from pathlib import Path
from docx import Document


class FileReader:
    """Reads plain text from .txt and .docx files."""

    def read(self, filepath: str) -> str:
        path = Path(filepath)
        if not path.exists():
            return "ERROR: File not found."
        if path.suffix.lower() == ".txt":
            return self._txt(path)
        elif path.suffix.lower() == ".docx":
            return self._docx(path)
        return "ERROR: Unsupported file type. Use .txt or .docx"

    def _txt(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return path.read_text(encoding="latin-1")
        except Exception as e:
            return f"ERROR: {e}"

    def _docx(self, path: Path) -> str:
        try:
            doc = Document(str(path))
            return "\n\n".join(
                p.text for p in doc.paragraphs if p.text.strip()
            )
        except Exception as e:
            return f"ERROR: {e}"

