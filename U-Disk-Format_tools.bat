@echo off
MODE con: COLS=160 LINES=50
set filepath=%~dp0
cd %filepath%
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"  
if '%errorlevel%' NEQ '0' (  
echo request Admin Access...  
goto UACPrompt  
) else ( goto gotAdmin )   
:UACPrompt   
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"  
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"  
"%temp%\getadmin.vbs"  
exit /B  
:gotAdmin
cls
python run.py
pause;