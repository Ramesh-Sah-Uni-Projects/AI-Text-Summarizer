# Text Summarization Chatbot
Test summarization chatbot is AI based chatbot. It summarize the large volume of text into the short form. It is summarize according to the user instruction words count

---

## Model Used
phi3:mini — lightweight model.

## Link to project video recording: https://youtu.be/ze_hP_chNO0

---

# AI Text Summarizer

A fully offline, AI-powered chatbot that summarizes large volumes of text
into concise summaries. It uses the **phi3:mini** model via **Ollama**
and runs entirely on the local machine — no internet required.

Available in two modes:
- **Terminal chatbot** — `run_chatbot.py` (NLP assignment entry point)
- **GUI desktop app** — `app.py` (built with Tkinter)

---

## NLP Assignment Compliance

This project follows the assignment template at
`GuGriffin/NLP_Assisgnment`.

| Requirement | Status | Where |
|---|---|---|
| Inherits from `ChatbotBase` | ✅ | `chatbot.py` line `class ChatBot(ChatbotBase):` |
| Calls `super().__init__()` | ✅ | `chatbot.py` constructor |
| Overrides `greeting()` | ✅ | `chatbot.py` |
| Overrides `farewell()` | ✅ | `chatbot.py` |
| Overrides `conversation_is_active()` | ✅ | `chatbot.py` |
| Overrides `receive_input()` | ✅ | `chatbot.py` |
| Overrides `process_input()` | ✅ | `chatbot.py` |
| Overrides `generate_response()` | ✅ | `chatbot.py` |
| Overrides `respond()` | ✅ | `chatbot.py` |
| Entry point `run_chatbot.py` | ✅ | top-level |
| ≥ 3 git commits | ✅ | see commit history |
| Inheritance verified by unit test | ✅ | `test_all.py::test_inherits_chatbot_base` |

---

## Features

- Paste text or upload `.txt` / `.docx` files
- Choose summary length (50 / 75 / 100 words, or any number you type)
- Streams output word by word in real time
- Follow-up commands: `bullet points`, `simpler`, `one sentence`, `academic`
- Copy summary to clipboard with one click (GUI)
- Full conversation history within the session
- Fully offline — no data sent over the internet

---

## Model Used

| Model | Description |
|---|---|
| `phi3:mini` | Lightweight LLM (~2.3 GB), runs on 4 GB RAM laptops |

---

## Project Structure

| File | Purpose |
|---|---|
| `chatbot_base.py` | Base chatbot class (exact assignment template — unmodified) |
| `chatbot.py` | `ChatBot` class — inherits from `ChatbotBase`, overrides all required methods |
| `run_chatbot.py` | Terminal entry point for the chatbot |
| `app.py` | GUI desktop app (Tkinter) |
| `summariser.py` | AI summarisation using phi3:mini via Ollama |
| `file_reader.py` | Reads `.txt` and `.docx` files |
| `test_all.py` | Unit tests (Summariser, ChatBot inheritance, FileReader) |
| `environment.yml` | Conda environment config |
| `run.bat` | Windows launcher (GUI / Terminal / Tests) |

---

## First Time Setup (only once)

**1. Install Ollama**

Download from <https://ollama.com>, then run:
```bash
ollama pull phi3:mini
```

**2. Create Conda environment**
```bash
conda env create -f environment.yml
conda activate chatbot
```

---

## How to Run

### Option A — Terminal chatbot (NLP assignment entry point)
```bash
conda activate chatbot
python run_chatbot.py
```

### Option B — GUI app
```bash
conda activate chatbot
python app.py
```

### Option C — Double-click `run.bat` (Windows)
Choose from the menu:
- `1` — Launch GUI App
- `2` — Launch Terminal Chatbot
- `3` — Run Tests

### Option D — VS Code
1. Open folder in VS Code
2. `Ctrl+Shift+P` → Python: Select Interpreter
3. Choose: `Python 3.12 ('chatbot': conda)`
4. Open terminal → `python run_chatbot.py` or `python app.py`

---

## How to Use — Terminal Chatbot

```
Type 'paste'         — Enter text to summarize
Type '75 words'      — Summarize in 75 words
Type 'bullet points' — Format as bullet points
Type 'simpler'       — Use simpler language
Type 'one sentence'  — Condense to one sentence
Type 'academic'      — Use formal academic language
Type 'history'       — View conversation history
Type 'clear'         — Reset text and history
Type 'help'          — Show all commands
Type 'quit'          — Exit
```

### Example session
```
You: paste
Paste your text below. Press Enter twice when finished:
<paste your article here>
<blank line>

Bot: Text loaded — 312 words. Now type an instruction.

You: 75 words bullet points
Bot: • Key point one ...
     • Key point two ...

You: simpler
Bot: <simplified version streams here>

You: quit
Goodbye!
```

---

## How to Use — GUI

1. Paste large text into the left panel, or click **Upload File** to load `.txt` / `.docx`
2. Choose word count: **50 / 75 / 100**
3. Click **Summarise** — output streams word by word
4. Type a follow-up and click **Send** to refine
5. Click **Copy** to copy the summary to clipboard

---

## Run Tests

```bash
python test_all.py
```

Covers:
- `Summariser` — word-count parsing, format detection, offline fallback
- `ChatBot` — inheritance from `ChatbotBase`, all overridden methods, history management
- `FileReader` — txt / docx / error handling

---

## Class Design — Methods Overridden from `ChatbotBase`

| Method | What it does in `ChatBot` |
|---|---|
| `__init__(name)` | Calls `super().__init__()`, removes the shadowing `conversation_is_active` attribute, sets `_active` flag, creates `Summariser` and `FileReader` instances, initialises history |
| `greeting()` | Prints welcome banner and command list |
| `farewell()` | Prints goodbye and shows count of summaries generated this session |
| `conversation_is_active()` | Returns `self._active` (True while session running) |
| `receive_input()` | Reads from terminal with `\nYou: ` prompt; handles Ctrl+C as 'quit' |
| `process_input(user_input)` | Parses input into an action dict: quit / paste / summarise / clear / history / help / unknown |
| `generate_response(processed_input)` | Executes the action — including streaming AI summaries via Ollama |
| `respond(out_message)` | One full conversation turn: print previous → input → process → generate |

---

## System Requirements

- Windows 10 / 11, macOS, or Linux
- Anaconda or Miniconda
- Ollama installed and running
- 4 GB RAM minimum (8 GB recommended)
- ~3 GB free disk space (for phi3:mini model)

---
## GUI of screen: <img width="1905" height="982" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/802f34f9-02e0-4450-a8b9-fc04d33049c4" />

