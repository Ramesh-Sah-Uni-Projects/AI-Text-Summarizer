# AI Text Summarizer

> A fully offline, AI-powered chatbot that condenses large volumes of text into concise, customizable summaries — powered by `phi3:mini` via Ollama.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Model](https://img.shields.io/badge/Model-phi3%3Amini-purple)
![Offline](https://img.shields.io/badge/Mode-Offline-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

---

## Overview

**AI Text Summarizer** is a local, privacy-first chatbot that transforms long-form text into clear, length-controlled summaries. It runs entirely on your machine — no API keys, no internet, no data ever leaves your device.

The application is available in two modes:

- **Terminal chatbot** (`run_chatbot.py`) — the NLP assignment entry point
- **GUI desktop app** (`app.py`) — a Tkinter-based graphical interface

**Project demo:** [Watch on YouTube](https://youtu.be/ze_hP_chNO0)

---

## Table of Contents

1. [Features](#features)
2. [Screenshots](#screenshots)
3. [Model](#model)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Running the Application](#running-the-application)
7. [Usage Guide](#usage-guide)
8. [Testing](#testing)
9. [Class Design](#class-design)
10. [NLP Assignment Compliance](#nlp-assignment-compliance)
11. [System Requirements](#system-requirements)

---

## Features

- **Flexible input** — paste text directly or upload `.txt` / `.docx` files
- **Adjustable length** — choose 50, 75, or 100 words, or specify any custom count
- **Real-time streaming** — summaries appear word-by-word as the model generates them
- **Follow-up refinement** — commands such as `bullet points`, `simpler`, `one sentence`, and `academic`
- **One-click copy** — copy summaries to clipboard from the GUI
- **Session history** — full conversation log retained within each session
- **100% offline** — no network connection required at runtime

---

## Screenshots

<img width="1905" height="982" alt="GUI Screenshot" src="https://github.com/user-attachments/assets/802f34f9-02e0-4450-a8b9-fc04d33049c4" />

---

## Model

| Model        | Size    | Notes                                                  |
| ------------ | ------- | ------------------------------------------------------ |
| `phi3:mini`  | ~2.3 GB | Lightweight LLM — runs comfortably on 4 GB RAM laptops |

---

## Project Structure

| File              | Purpose                                                                       |
| ----------------- | ----------------------------------------------------------------------------- |
| `chatbot_base.py` | Base chatbot class (assignment template — unmodified)                         |
| `chatbot.py`      | `ChatBot` class inheriting from `ChatbotBase`; overrides all required methods |
| `run_chatbot.py`  | Terminal entry point                                                          |
| `app.py`          | Tkinter GUI desktop application                                               |
| `summariser.py`   | AI summarisation logic using `phi3:mini` via Ollama                           |
| `file_reader.py`  | File loader for `.txt` and `.docx` formats                                    |
| `test_all.py`     | Unit tests for the Summariser, ChatBot, and FileReader modules                |
| `environment.yml` | Conda environment specification                                               |
| `run.bat`         | Windows launcher (GUI / Terminal / Tests)                                     |

---

## Installation

### 1. Install Ollama

Download Ollama from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull phi3:mini
```

### 2. Create the Conda environment

```bash
conda env create -f environment.yml
conda activate chatbot
```

---

## Running the Application

### Option A — Terminal Chatbot *(NLP assignment entry point)*

```bash
conda activate chatbot
python run_chatbot.py
```

### Option B — GUI Application

```bash
conda activate chatbot
python app.py
```

### Option C — Windows Launcher

Double-click `run.bat` and choose from the menu:

| Option | Action                  |
| ------ | ----------------------- |
| `1`    | Launch GUI App          |
| `2`    | Launch Terminal Chatbot |
| `3`    | Run Tests               |

### Option D — VS Code

1. Open the project folder in VS Code.
2. Press `Ctrl + Shift + P` → **Python: Select Interpreter**.
3. Select **Python 3.12 ('chatbot': conda)**.
4. Open the integrated terminal and run either `python run_chatbot.py` or `python app.py`.

---

## Usage Guide

### Terminal Commands

| Command          | Description                          |
| ---------------- | ------------------------------------ |
| `paste`          | Enter text to summarize              |
| `75 words`       | Generate a 75-word summary           |
| `bullet points`  | Format the output as bullet points   |
| `simpler`        | Rewrite using simpler language       |
| `one sentence`   | Condense the summary to one sentence |
| `academic`       | Use formal academic phrasing         |
| `history`        | View the conversation history        |
| `clear`          | Reset the current text and history   |
| `help`           | Display all available commands       |
| `quit`           | Exit the chatbot                     |

### Example Session

```text
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

### GUI Workflow

1. Paste text into the left panel, or click **Upload File** to load a `.txt` or `.docx` file.
2. Choose a summary length — **50**, **75**, or **100** words.
3. Click **Summarise** to begin streaming the result.
4. Type a follow-up instruction and click **Send** to refine the output.
5. Click **Copy** to copy the final summary to your clipboard.

---

## Testing

Run the full test suite with:

```bash
python test_all.py
```

The suite covers:

- **Summariser** — word-count parsing, format detection, and offline fallback
- **ChatBot** — inheritance from `ChatbotBase`, all overridden methods, and history management
- **FileReader** — `.txt` parsing, `.docx` parsing, and error handling

---

## Class Design

The `ChatBot` class inherits from `ChatbotBase` and overrides each required method:

| Method                          | Responsibility                                                                                                                                                                     |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__init__(name)`                | Calls `super().__init__()`, clears the shadowing `conversation_is_active` attribute, sets the `_active` flag, instantiates `Summariser` and `FileReader`, and initialises history. |
| `greeting()`                    | Prints the welcome banner and command list.                                                                                                                                        |
| `farewell()`                    | Prints a goodbye message with the number of summaries generated in the session.                                                                                                    |
| `conversation_is_active()`      | Returns `self._active` — `True` while the session is running.                                                                                                                      |
| `receive_input()`               | Reads from the terminal using the `\nYou: ` prompt; treats `Ctrl + C` as `quit`.                                                                                                   |
| `process_input(user_input)`     | Parses input into an action dictionary: `quit`, `paste`, `summarise`, `clear`, `history`, `help`, or `unknown`.                                                                    |
| `generate_response(processed)`  | Executes the resolved action — including streaming AI summaries via Ollama.                                                                                                        |
| `respond(out_message)`          | Drives one full conversation turn: print → receive → process → generate.                                                                                                           |

---

## NLP Assignment Compliance

This project conforms to the template at `GuGriffin/NLP_Assisgnment`.

| Requirement                                | Status | Location                                              |
| ------------------------------------------ | :----: | ----------------------------------------------------- |
| Inherits from `ChatbotBase`                |   ✅   | `chatbot.py` — `class ChatBot(ChatbotBase):`          |
| Calls `super().__init__()`                 |   ✅   | `chatbot.py` constructor                              |
| Overrides `greeting()`                     |   ✅   | `chatbot.py`                                          |
| Overrides `farewell()`                     |   ✅   | `chatbot.py`                                          |
| Overrides `conversation_is_active()`       |   ✅   | `chatbot.py`                                          |
| Overrides `receive_input()`                |   ✅   | `chatbot.py`                                          |
| Overrides `process_input()`                |   ✅   | `chatbot.py`                                          |
| Overrides `generate_response()`            |   ✅   | `chatbot.py`                                          |
| Overrides `respond()`                      |   ✅   | `chatbot.py`                                          |
| Entry point `run_chatbot.py`               |   ✅   | top-level                                             |
| ≥ 3 git commits                            |   ✅   | see commit history                                    |
| Inheritance verified by unit test          |   ✅   | `test_all.py::test_inherits_chatbot_base`             |

---

## System Requirements

- **Operating System:** Windows 10/11, macOS, or Linux
- **Python Environment:** Anaconda or Miniconda
- **Runtime:** Ollama (installed and running)
- **Memory:** 4 GB RAM minimum (8 GB recommended)
- **Disk Space:** ~3 GB free (for the `phi3:mini` model)

---
