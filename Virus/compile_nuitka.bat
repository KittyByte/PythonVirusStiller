@echo off

python -m nuitka --windows-disable-console --follow-imports --windows-icon-from-ico=icon.ico "Stiller.py"

rmdir /s /q Stiller.build
del "Stiller.cmd"

:cmd
pause null