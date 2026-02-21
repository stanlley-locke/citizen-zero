# ID Service API Reference

The Identity Service is the primary authority for digital identity management within the Citizen Zero ecosystem.

## Base URL
`http://<host>:8001/api/v1/`

## Endpoints

### 1. Digital ID Management

#### List/Retrieve IDs
- **GET** `/ids/`
- **GET** `/ids/{id}/`
Retrieves the cryptographic representation of a digital identity.

#### Identity Analytics
- **GET** `/ids/analytics/`
Returns key performance indicators (KPIs) for the dashboard, including total issued IDs, pending reviews, and demographic distributions.

### 2. Document Generation

#### Document Preview
- **GET** `/documents/preview/?type={type}&citizen_id={id}`
Generates a real-time PDF preview. Supported types: `national_id`, `passport`, `birth_certificate`.

#### Document Download
- **GET** `/documents/download/?type={type}&citizen_id={id}`
Generates and serves a PDF file for local storage.

### 3. Issuance Requests

#### Submit Request
- **POST** `/requests/`
Submits a new request for identity issuance. Requires citizen metadata and supporting documentation handles.

#### Check Status
- **GET** `/requests/{request_id}/`
Returns the current processing status (PENDING, APPROVED, REJECTED).

### 4. System Health
- **GET** `/health/`
Returns the operational status of the ID service and its database connection.

## Data Formats
- **Payloads**: JSON
- **Identity Records**: ISO 18013-5 / CBOR
- **Documents**: PDF (Application/PDF)
