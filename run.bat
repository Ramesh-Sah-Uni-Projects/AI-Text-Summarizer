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
