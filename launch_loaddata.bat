%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call python manage.py loaddata feedcrunch_dump8.json
PAUSE;
