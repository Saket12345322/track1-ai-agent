@echo off
echo Starting AI Agent...
cd /d "D:\GEN AI\track 1"
pip install flask flask-cors groq -q
python main.py
pause
