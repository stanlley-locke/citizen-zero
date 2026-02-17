# Starting Backend Services

This guide outlines the ports and commands required to run the Citizen Zero backend ecosystem and connect it to the Flutter Android app.

## 1. Service Port Mappings

| Service Name    | Port | Description                          | Path                                      |
|:----------------|:-----|:-------------------------------------|:------------------------------------------|
| **Auth**        | 8000 | Authentication & Admin Management    | `backend/services/auth-service`           |
| **ID**          | 8001 | Digital ID Issuance & Requests       | `backend/services/id-service`             |
| **Verify**      | 8002 | credential Verification              | `backend/services/verify-service`         |
| **Audit**       | 8003 | System Audit Logs                    | `backend/services/audit-service`          |
| **IPRS (Mock)** | 8005 | Citizen Registry Mock                | `backend/iprs-mock`                       |

## 2. Running Services

Open 5 separate terminal tabs/windows and run the following commands in each:

### Terminal 1: Auth Service
```bash
cd services/auth-service
python manage.py runserver 0.0.0.0:8000
```

### Terminal 2: ID Service
```bash
cd services/id-service
python manage.py runserver 0.0.0.0:8001
```

### Terminal 3: Verify Service
```bash
cd services/verify-service
python manage.py runserver 0.0.0.0:8002
```

### Terminal 4: Audit Service
```bash
cd services/audit-service
python manage.py runserver 0.0.0.0:8003
```

### Terminal 5: IPRS Mock
```bash
cd iprs-mock
python manage.py runserver 0.0.0.0:8005
```

---

## 3. Android Emulator Connectivity (ADB Reverse)

To allow the Android Emulator to access these `localhost` ports, you must run `adb reverse`. This maps the emulator's internal ports to your computer's ports.

**Run this command whenever you restart the emulator or plug in a physical device:**

```bash
adb reverse tcp:8000 tcp:8000
adb reverse tcp:8001 tcp:8001
adb reverse tcp:8002 tcp:8002
adb reverse tcp:8003 tcp:8003
adb reverse tcp:8005 tcp:8005
```

### Troubleshooting
*   **"Connection Refused"**: Ensure the service is running AND you have run the `adb reverse` command for that specific port.
*   **"Port already in use"**: Kill any existing python processes or change the port in the `runserver` command (and update `adb reverse` accordingly).
