%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
:: https://docs.djangoproject.com/en/dev/howto/deployment/checklist/
call python manage.py check --deploy
PAUSE;
