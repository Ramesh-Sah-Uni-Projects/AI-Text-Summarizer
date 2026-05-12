# Text Summarization Chatbot
Test summarization chatbot is AI based chatbot. It summarize the large volume of text into the short form. It is summarize according to the user instruction words count

---

## Model Used
phi3:mini — lightweight model.

---

## Run in VS Code

1. Open VS Code
2. File > Open Folder > select AI_TEXT_Summarizer folder
3. Press Ctrl+Shift+P > Python: Select Interpreter
4. Choose: Python 3.12 ('chatbot': conda)
5. Press Ctrl+` to open terminal
6. Type:

    conda activate chatbot
    python app.py

---

## Run in Anaconda Prompt

    conda activate chatbot
    cd (project location) like: cd C:\Users\rames\Downloads\FinalProject
    python app.py

Or double-click run.bat

---

## First time setup (only once)

    ollama pull phi3:mini
    conda env create -f environment.yml
    conda activate chatbot

---

## How to use

1. Paste large text into the dark left panel
2. Or click Upload File for .txt or .docx
3. Choose 50 / 75 / 100 words
4. Click Summarise - streams instantly word by word
5. Follow-up: bullet points / simpler / one sentence

---

## Run tests

    python test_all.py

---

## Files

| File | Purpose |
| app.py | Main GUI window |
| summariser.py | AI summarisation (phi3:mini) |
| chatbot.py | Conversation history |
| file_reader.py | Reads .txt and .docx |
| test_all.py | Unit tests |
| environment.yml | Conda environment |
| run.bat | Windows quick launch |

## **GUI of App**
<img width="1905" height="982" alt="Screenshot (59)" src="https://github.com/user-attachments/assets/14a18bba-2248-4e7a-8d35-053a35a55b92" />

