%~d1
cd "%~p1"
cd "../.."
call venv\Scripts\activate.bat
call pip install --upgrade pip
call pip install "lib_bin\windows\lxml-3.7.3-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\scipy-0.19.0-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\scikit_learn-0.18.1-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\pycrypto-2.7a2-cp36-cp36m-win_amd64.whl"
call pip install "lib_bin\windows\Pillow-4.0.0-cp36-cp36m-win_amd64.whl"
call python "lib_bin\repositories\django-q-master\setup.py" install
call pip install -r requirements.txt
PAUSE;
