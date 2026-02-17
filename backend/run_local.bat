@echo off
echo Starting Citizen Zero Backend Services...

REM Start Auth Service
start "Auth Service (8000)" cmd /k "cd services\auth-service && python manage.py runserver 0.0.0.0:8000"

REM Start ID Service
start "ID Service (8001)" cmd /k "cd services\id-service && python manage.py runserver 0.0.0.0:8001"

REM Start Verify Service
start "Verify Service (8002)" cmd /k "cd services\verify-service && python manage.py runserver 0.0.0.0:8002"

echo Services started in new windows.
echo Auth:   http://127.0.0.1:8000
echo ID:     http://127.0.0.1:8001
echo Verify: http://127.0.0.1:8002
