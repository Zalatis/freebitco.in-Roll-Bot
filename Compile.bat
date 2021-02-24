pyinstaller -i "%cd%\compile\icon.ico" --onefile roll.py
cd %cd%\dist
ren roll.exe Roll-Bot.exe
robocopy %cd% ..\ Roll-Bot.exe /move
exit