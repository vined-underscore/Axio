@echo off
title Axio Setup
setlocal enabledelayedexpansion
set "folderPath=./data/"
for /d %%i in ("%folderPath%\*") do (
    rd /s /q "%%i"
)

set "folderPath=./configs/"
for /d %%i in ("%folderPath%\*") do (
    rd /s /q "%%i"
)

echo Cleaned ./data and ./configs
timeout /t 2 >nul
cls
echo Installing requirements...
timeout /t 1 >nul
python -m pip install -r requirements.txt
timeout /t 1 >nul
cls
echo Set up Axio.
echo You can now set the account tokens in ./configs/tokens.json and run axio.py
pause