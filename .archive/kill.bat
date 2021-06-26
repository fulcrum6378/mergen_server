FOR /F "tokens=5" %%T IN ('netstat -a -n -o ^| findstr %~1 ') DO (SET /A ProcessId=%%T)
taskkill /f /pid %ProcessId%
