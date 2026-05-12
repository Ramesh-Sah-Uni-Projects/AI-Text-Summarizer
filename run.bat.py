"""
:: ═══════════════════════════════════════════════════════════════════════
::                  TEXT SUMMARIZER  —  LAUNCHER SCRIPT
:: ═══════════════════════════════════════════════════════════════════════
::
:: WHAT THIS SCRIPT DOES
:: ---------------------
:: This is a Windows batch file (.bat) that launches the Text Summarizer
:: app with a single double-click — so the user does not have to open
:: a terminal and type commands manually.
::
:: HOW IT WORKS  (line by line)
:: ----------------------------
::
::   @echo off
::       Hides the command lines from the console window so only the
::       banner and app output are visible — keeps the window clean.
::
::   title Text Summarizer
::       Sets the title of the console window to "Text Summarizer"
::       (the text shown on the window's top bar and in the taskbar).
::
::   echo ==========================================
::   echo  Text Summarization Chatbot
::   echo  Make sure Ollama is open first!
::   echo ==========================================
::   echo.
::       Prints a friendly banner reminding the user that OLLAMA must
::       be running before the app starts. Ollama is the local AI
::       engine that powers the summariser — if it is not open, the
::       app will not be able to generate summaries.
::       The final "echo." just prints an empty line for spacing.
::
::   call conda activate chatbot
::       Switches into the "chatbot" Conda environment, where all the
::       Python libraries (tkinter helpers, ollama client, docx reader,
::       etc.) are installed. "call" is used so the script keeps running
::       after Conda finishes activating.
::
::   cd /d "%~dp0"
::       Changes the working directory to the folder where this .bat
::       file lives. "%~dp0" means "the drive + path of this script"
::       and the "/d" flag allows switching drives if needed. This
::       ensures Python can find app.py no matter where the user
::       double-clicks the file from.
::
::   python app.py
::       Finally runs the main application — this opens the Tkinter
::       window and starts the summarizer.
::
:: WHY IT MATTERS
:: --------------
:: This script makes the app feel like a normal desktop program.
:: The user does not need to know Python, Conda, or the command line —
:: they just double-click the file and the summarizer opens.
::
:: ═══════════════════════════════════════════════════════════════════════
"""

@echo off
title Text Summarizer
echo ==========================================
echo  Text Summarization Chatbot
echo  Make sure Ollama is open first!
echo ==========================================
echo.
call conda activate chatbot
cd /d "%~dp0"
python app.py
