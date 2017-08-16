%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
pip freeze > requirements.txt