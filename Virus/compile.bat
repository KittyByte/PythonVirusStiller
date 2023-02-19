@echo off

pyinstaller --noconfirm --onefile --windowed --version-file "version.py" --icon "drawing.ico" "Stiller.py"

rmdir /s /q build
del "Stiller.spec"

:cmd
pause null