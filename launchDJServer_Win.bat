%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call cmd /k heroku local web -f Procfile.windows
PAUSE;
