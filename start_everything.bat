@echo off
echo 🚀 Starting Creator Insight Platform...
echo.

echo 📋 Starting Flask API...
start cmd /k "venv\Scripts\activate && python app.py"

echo ⏳ Waiting for API to start...
timeout /t 5 /nobreak

echo 📊 Starting Dashboard...
call venv\Scripts\activate
streamlit run dashboard.py

echo.
echo ✅ Both services should be running!
echo.
pause