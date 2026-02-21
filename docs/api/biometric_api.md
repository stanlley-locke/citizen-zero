# Biometric Service API Reference

The Biometric Service handles identity verification through facial and fingerprint analysis.

## Base URL
`http://<host>:8002/api/v1/`

## Endpoints

### 1. Face Matching

#### Initiate Match
- **POST** `/matching/face/`
  - **Body**: `{ "citizen_id": "string", "image_b64": "string" }`
  - **Returns**: A task ID for tracking.
Asynchronously matches a face capture against the stored template.

#### Check Match Result
- **GET** `/matching/face/{task_id}/`
Returns the match score and binary result (match/no-match).

### 2. Liveness Detection

#### Verify Liveness
- **POST** `/verification/liveness/`
  - **Body**: `{ "video_b64": "string", "session_id": "string" }`
Performs texture and micro-expression analysis to detect spoofs/deepfakes.

### 3. Template Management
- **POST** `/biometrics/enroll/`
Captures and hashes new biometric templates for the foundational ID.

## Task States
1. **PENDING**: Task is in the Celery queue.
2. **PROCESSING**: Task is being handled by a worker (GPU inference).
3. **COMPLETED**: Result is available.
4. **FAILED**: An error occurred during biometric analysis.
