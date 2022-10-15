cd /d %~dp0

@echo off

SET /P input="Às‚µ‚Ü‚·‚©(y/n)"
IF %input% == n GOTO :END
IF %input% == N GOTO :END

rem  py -3.8 -m venv db1   ‰¼‘zŠÂ‹«ì¬—v

call C:\pyenv\db1\Scripts\activate & cd C:\tmp  & python copy_¬“ú’ö.py
pause


