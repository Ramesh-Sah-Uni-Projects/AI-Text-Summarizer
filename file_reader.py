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
