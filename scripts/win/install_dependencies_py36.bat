%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call pip install --upgrade pip
call pip install "lib_bin\windows\lxml-3.7.3-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\scipy-0.19.0-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\scikit_learn-0.18.1-cp36-cp36m-win_amd64.whl"
call pip install https://github.com/hairychris/django-material/archive/2b3d70347cf29bcc02b06d3319f9617b626502c8.zip
call pip install -r requirements.txt
PAUSE;
