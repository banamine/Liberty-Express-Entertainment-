@echo off
echo Installing M3U Matrix CDS v5.0...

:: Create folder
mkdir "%USERPROFILE%\Desktop\M3U Matrix CDS v5.0"
cd /d "%~dp0"

:: Copy files
xcopy /E /Y * "%USERPROFILE%\Desktop\M3U Matrix CDS v5.0\" >nul

:: Create start script
echo @echo off > "%USERPROFILE%\Desktop\M3U Matrix CDS v5.0\START.bat"
echo python main.py >> "%USERPROFILE%\Desktop\M3U Matrix CDS v5.0\START.bat"
echo pause >> "%USERPROFILE%\Desktop\M3U Matrix CDS v5.0\START.bat"

echo Done! Open START.bat
pause