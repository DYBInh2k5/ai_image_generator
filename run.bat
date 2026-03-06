@echo off
echo =========================================
echo DreamForge AI Local Image Generator
echo =========================================

echo 1. Installing required Python libraries for Local AI...
echo NOTE: PyTorch and Diffusers are large packages (~2-4GB total).
echo This may take a few minutes.
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies. Please ensure Python is installed.
    pause
    exit /b %errorlevel%
)

echo.
echo 2. Starting Local FastAPI Backend server...
echo NOTE: The first run will download the actual AI Model (~4GB). Please be patient.
start "DreamForge Local Backend" cmd /c "python -m uvicorn server:app --port 8001 --reload"

echo.
echo 3. Opening the web interface...
timeout /t 5 /nobreak > nul
start index.html

echo.
echo =========================================
echo Setup complete! The backend API is starting in a separate window.
echo Wait until it says "Model successfully loaded into memory" before generating.
echo =========================================
pause
