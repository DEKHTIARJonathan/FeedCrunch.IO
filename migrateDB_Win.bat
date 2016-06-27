%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call python manage.py makemigrations feedradar
call python manage.py migrate
call python manage.py load_data
PAUSE;
