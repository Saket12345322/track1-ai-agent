@echo off
echo Starting AI Agent...
cd /d "D:\GEN AI\track 1"
pip install flask flask-cors groq -q
start python main.py
timeout /t 3
echo Starting ngrok tunnel...
.\ngrok http 8080
pause
