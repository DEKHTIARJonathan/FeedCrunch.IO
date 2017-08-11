%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call pip install --upgrade pip
call pip install "lib_bin\windows\scipy-0.19.1-cp35-cp35m-win_amd64.whl"
REM call pip install https://github.com/hairychris/django-material/archive/2b3d70347cf29bcc02b06d3319f9617b626502c8.zip
call pip install -r requirements.txt
PAUSE;
