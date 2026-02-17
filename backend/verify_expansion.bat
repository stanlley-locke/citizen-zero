@echo off
echo ========================================================
echo CITIZEN ZERO - BACKEND EXPANSION VERIFICATION
echo ========================================================

echo.
echo [1/3] APPLYING MIGRATIONS
echo --------------------------------------------------------

echo [ID SERVICE] Applying Migrations...
cd services\id-service
python manage.py makemigrations
python manage.py migrate
cd ..\..

echo [AUDIT SERVICE] Applying Migrations...
cd services\audit-service
python manage.py makemigrations
python manage.py migrate
cd ..\..

echo.
echo [2/3] TESTING ID SERVICE (Port 8001)
echo --------------------------------------------------------
echo Request: Issuing Persistent ID for 12345678...
curl -X POST http://127.0.0.1:8001/api/v1/id/issue/ -H "Content-Type: application/json" -d "{\"citizen_id\": \"12345678\"}"
echo.

echo.
echo Request: Listing Credentials for 12345678...
curl -X GET "http://127.0.0.1:8001/api/v1/id/credentials/?citizen_id=12345678"
echo.

echo.
echo [3/3] TESTING AUDIT SERVICE (Port 8003)
echo --------------------------------------------------------
echo Request: Checking Audit Kernel Logs...
curl -X GET http://127.0.0.1:8003/api/v1/audit/logs/
echo.

echo.
echo ========================================================
echo VERIFICATION COMPLETE
echo ========================================================
pause
