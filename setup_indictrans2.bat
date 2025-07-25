@echo off
echo Setting up IndicTrans2 environment...
echo.

REM Install additional dependencies
echo Installing additional dependencies...
pip install sentencepiece sacremoses mosestokenizer ctranslate2 regex nltk
if %ERRORLEVEL% neq 0 (
    echo Warning: Some dependencies failed to install
    echo This is normal on Windows without Visual C++ Build Tools
)

REM Install indic-nlp-library
echo Installing indic-nlp-library...
pip install git+https://github.com/anoopkunchukuttan/indic_nlp_library
if %ERRORLEVEL% neq 0 (
    echo Warning: indic-nlp-library installation failed
    echo You may need Visual C++ Build Tools
)

REM Create model directory
echo Creating model directory...
if not exist "models\indictrans2" mkdir "models\indictrans2"

REM Create instructions file
echo Creating setup instructions...
echo # IndicTrans2 Model Setup > models\indictrans2\SETUP.txt
echo. >> models\indictrans2\SETUP.txt
echo To use real IndicTrans2 models: >> models\indictrans2\SETUP.txt
echo 1. Visit: https://github.com/AI4Bharat/IndicTrans2#download-models >> models\indictrans2\SETUP.txt
echo 2. Download model files to this directory >> models\indictrans2\SETUP.txt
echo 3. Set MODEL_TYPE=indictrans2 in .env >> models\indictrans2\SETUP.txt
echo 4. Restart your backend >> models\indictrans2\SETUP.txt

echo.
echo ✅ Setup completed!
echo.
echo Next steps:
echo 1. Check models\indictrans2\SETUP.txt for model download instructions
echo 2. Your app will run in mock mode until real models are downloaded
echo 3. Start backend: cd backend ^&^& python main.py
echo 4. Start frontend: cd frontend ^&^& streamlit run app.py
echo.
pause
