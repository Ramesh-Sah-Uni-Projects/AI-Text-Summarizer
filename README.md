# AI Text Summarizer

A fully offline AI-powered desktop app that summarizes large text into 
concise summaries using phi3:mini via Ollama. Paste text or upload a file, 
pick a word count, and get an instant summary — no internet required.

---

## Features

- Paste text or upload `.txt` / `.docx` files
- Choose summary length: 50 / 75 / 100 words
- Streams output word by word in real time
- Follow-up prompts: bullet points / simpler / one sentence
- Copy summary to clipboard with one click
- Fully offline — no data sent to the internet

---

## Model Used

| Model | Description |
|---|---|
| `phi3:mini` | Lightweight LLM, works on 4GB RAM laptops |

---

## First Time Setup (only once)

**1. Install Ollama**

Download from https://ollama.com then run:
```bash
ollama pull phi3:mini
```

**2. Create Conda Environment**
```bash
conda env create -f environment.yml
conda activate chatbot
```

---

## How to Run

**Option A — Double click**

**Option B — Anaconda Prompt**
```bash
conda activate chatbot
cd (file location). example: cd C:\Users\rames\Downloads\FinalProject
python app.py
```

**Option C — VS Code**
1. Open folder in VS Code
2. `Ctrl+Shift+P` → Python: Select Interpreter
3. Choose: `Python 3.12 (chatbot: conda)`
4. Open terminal → `python app.py`

---

## How to Use

1. Paste large text into the dark left panel
2. Or click **Upload File** to load a `.txt` or `.docx` document
3. Choose word count: **50 / 75 / 100 words**
4. Click **Summarise** — streams instantly word by word
5. Type a follow-up instruction and click **Send** to refine:
   - `bullet points`
   - `simpler language`
   - `one sentence`

---

## Project Structure

| File | Purpose |
|---|---|
| `app.py` | Main GUI window (Tkinter) |
| `summariser.py` | AI summarisation using phi3:mini |
| `chatbot.py` | Conversation history management |
| `file_reader.py` | Reads .txt and .docx files |
| `test_all.py` | Unit tests |
| `environment.yml` | Conda environment config |
| `run.bat` | Windows one-click launcher |

---

## Run Tests

```bash
python test_all.py
```

---

## Requirements

- Windows 10 / 11
- Anaconda or Miniconda
- Ollama installed and running
- 4GB RAM minimum


