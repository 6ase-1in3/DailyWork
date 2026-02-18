@echo off
cd /d "%~dp0"

call Local_Server\kill_server.bat

start "" http://127.0.0.1:8998
python Local_Server\server.py
pause
