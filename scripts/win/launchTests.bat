%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call coverage run manage.py test
call coverage report -m
call coverage html -i
PAUSE;
