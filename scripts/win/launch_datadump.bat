%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call python manage.py dumpdata --format=json --output application/fixtures/feedcrunch_dump8.json --indent 3 feedcrunch
PAUSE;
