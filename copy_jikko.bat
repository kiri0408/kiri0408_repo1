cd /d %~dp0

@echo off

SET /P input="���s���܂���(y/n)"
IF %input% == n GOTO :END
IF %input% == N GOTO :END

rem  py -3.8 -m venv db1   ���z���쐬�v

call C:\pyenv\db1\Scripts\activate & cd C:\tmp  & python copy_������.py
pause


