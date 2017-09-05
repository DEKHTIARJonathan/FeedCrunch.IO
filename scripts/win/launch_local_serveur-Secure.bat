%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call cmd /k python manage.py runserver_plus 0.0.0.0:5000 --cert ./
PAUSE;
