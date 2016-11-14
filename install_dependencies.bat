%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call pip install --upgrade pip
call pip install "lib_bin\windows\lxml-3.6.4-cp27-cp27m-win_amd64.whl" 
call pip install "lib_bin\windows\numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl"
call pip install "lib_bin\windows\scipy-0.18.1-cp27-cp27m-win_amd64.whl"
call pip install -r requirements-win.txt
PAUSE;
