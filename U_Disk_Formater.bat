@echo off
set filepath=%~dp0
cd %filepath%
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"  
if '%errorlevel%' NEQ '0' (  
echo RequestAdminAccess...  
goto UACPrompt  
) else ( goto gotAdmin )   
:UACPrompt   
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"  
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"  
"%temp%\getadmin.vbs"  
exit /B  
:gotAdmin  
python run.py
pause;