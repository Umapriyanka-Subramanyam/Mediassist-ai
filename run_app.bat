@echo off
echo Starting Backend...
start cmd /k "uvicorn backend.main:app --reload"

echo Starting Frontend...
start cmd /k "streamlit run frontend/app.py"

echo AI Medicine Assistant is running!
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:8501
