@echo off
echo Watching chatkit_server.log (Press Ctrl+C to stop)
echo ============================================
echo.
powershell -command "Get-Content chatkit_server.log -Wait -Tail 50"
