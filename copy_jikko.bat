cd /d %~dp0

@echo off

SET /P input="実行しますか(y/n)"
IF %input% == n GOTO :END
IF %input% == N GOTO :END

rem  py -3.8 -m venv db1   仮想環境作成要

call C:\pyenv\db1\Scripts\activate & cd C:\tmp  & python copy_小日程.py
pause


