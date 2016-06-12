%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call cmd /k pip install -r requirements.txt
PAUSE;
