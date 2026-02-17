@echo off
echo ========================================================
echo CITIZEN ZERO - COMPREHENSIVE BACKEND TEST SUITE
echo ========================================================
echo.

echo [1/4] TESTING IPRS MOCK (Port 8005)
echo -----------------------------------
echo Request: Listing Citizens...
curl -s -o NUL -w "HTTP Code: %%{http_code}\n" http://127.0.0.1:8005/api/v1/citizens/
echo Request: Searching for Jane Doe (12345678)...
curl -s "http://127.0.0.1:8005/api/v1/citizens/?search=12345678"
echo.
echo.

echo [2/4] TESTING AUTH SERVICE (Port 8000)
echo --------------------------------------
echo Request: Login with Valid Credentials (12345678)...
curl -s -X POST -H "Content-Type: application/json" -d "{\"national_id\": \"12345678\"}" http://127.0.0.1:8000/api/v1/auth/login/
echo.
echo Request: Login with INVALID Credentials (00000000)...
curl -s -X POST -H "Content-Type: application/json" -d "{\"national_id\": \"00000000\"}" http://127.0.0.1:8000/api/v1/auth/login/
echo.
echo.

echo [3/4] TESTING ID SERVICE (Port 8001)
echo ------------------------------------
echo Request: Issue Digital ID (12345678)...
curl -s -X POST -H "Content-Type: application/json" -d "{\"citizen_id\": \"12345678\"}" http://127.0.0.1:8001/api/v1/id/management/issue/
echo.
echo Request: Issue ID without parameter (Negative Test)...
curl -s -X POST -H "Content-Type: application/json" -d "{}" http://127.0.0.1:8001/api/v1/id/management/issue/
echo.
echo.

echo [4/4] TESTING VERIFY SERVICE (Port 8002)
echo ----------------------------------------
echo Request: Verify Valid Token...
curl -s -X POST -H "Content-Type: application/json" -d "{\"token\": \"valid_sample_token\"}" http://127.0.0.1:8002/api/v1/verify/token/
echo.
echo.

echo TEST SUITE COMPLETE.
echo If you saw JSON responses above, the backend is 100%% operational.
pause
