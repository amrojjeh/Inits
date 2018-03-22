@echo off
REM %~dp0 = the path the batch file resides in
REM %1 = First command line argument
call py -3 "%~dp0\PInit.py" %1 %2