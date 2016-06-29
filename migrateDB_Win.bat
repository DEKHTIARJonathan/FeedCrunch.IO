%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call python manage.py makemigrations feedcrunch
call python manage.py migrate
PAUSE;
