%~d1
cd "%~p1"
call venv\Scripts\activate.bat
call travis encrypt "feedcrunch:***********(token)********#********(channel Name)**********" --add notifications.slack.rooms
PAUSE;
