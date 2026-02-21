# Citizen Zero: Digital-First National Identity Ecosystem

**Citizen Zero** is a comprehensive, microservices-driven architecture designed for a next-generation National Identity Ecosystem. It leverages biometric verification, cryptographic security (COSE/CBOR), and privacy-preserving technologies (ZKP) to provide a secure, scalable, and digital-first identity platform.

---

## 🏗 System Architecture

The ecosystem is built using a decentralized microservices approach, ensuring high availability and separation of concerns.

### 🧩 Core Services (Backend)

| Service | Technology | Description |
| :--- | :--- | :--- |
| **ID Service** | Django, PostgreSQL | Manages the lifecycle of Digital IDs (Issuance, Revocation, Recovery). Implements ISO 18013-5 (mDL) standards. |
| **Biometric Service** | Django, Celery, Redis | Handles asynchronous biometric matching (Face, Fingerprint) and liveness detection for fraud prevention. |
| **Verify Service** | Django, ZKP | Provides online and offline verification endpoints. Includes Zero-Knowledge Proof (ZKP) provers for privacy-preserving checks. |
| **Monitor Service** | Django | Centralized dashboard for system health, database status, and network topology visualization. |
| **Shared** | Python | Common utilities for cryptography (AES/RSA), JWT handling, and middleware. |

### 💻 Client Applications

- **Desktop (Super Admin)**: A PyQt6-based management console for high-level administration, audit log viewing (CSV/Database), and system configuration.
- **Web Dashboards**:
    - **Admin Dashboard**: Vite/React-based UI for managing citizens, enrollment, and security logs.
    - **Employer Portal**: Portal for organizations to verify employees and manage KYC.
    - **Worker Dashboard**: Tools for field workers to register citizens and capture biometrics.
- **Mobile (Flutter)**:
    - **Citizen Wallet**: Secure storage for digital identity documents on Android/iOS.
    - **Verifier App**: Application for third-party agents to verify citizen identities.

---

## 🚀 Key Features

- **Standardized Identity**: Implements **ISO 18013-5** (Mobile Driving License) and **mDL** namespaces for global interoperability.
- **Cryptographic Integrity**: Uses **COSE (CBOR Object Signing and Encryption)** for secure document signing and verification.
- **Privacy-First**: Integrated **Zero-Knowledge Proofs (ZKP)** allow citizens to prove attributes (e.g., "Age > 18") without revealing their actual date of birth.
- **Biometric Fraud Prevention**: AI-driven face matching and **liveness detection** to mitigate deepfake and spoofing risks.
- **Operational Excellence**: Comprehensive **Ops CLI** for service deployment/scaling and an **Admin CLI** for managing identity records.

---

## 📂 Project Structure

```text
citizen-zero/
├── backend/            # Microservices (ID, Biometric, Verify, Monitor)
├── desktop/            # PyQt6 Admin & Config Management apps
├── web/                # React-based Dashboards (Admin, Employer, Worker)
├── flutter/            # Mobile Applications (Wallet, Verifier)
├── cli/                # Python-based Admin and Ops command-line tools
├── docs/               # Detailed API, Architecture, and User Guides
├── scripts/            # Deployment, Maintenance, and Setup scripts
└── research/           # Whitepapers and Executive Proposals
```

---

## 🛠 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- Flutter SDK
- Docker & Docker Compose
- Redis (for Celery)
- PostgreSQL

### 1. Backend Setup
Each service in `backend/services/` contains its own `requirements.txt` and `Dockerfile`.
```bash
cd backend/services/id-service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

### 2. Web Dashboards
```bash
cd web/admin-dashboard
npm install
npm run dev
```

### 3. Mobile Apps
```bash
cd flutter/citizen_wallet
flutter pub get
flutter run
```

---

## 📜 Documentation
For in-depth guides, please refer to the `docs/` directory:
- [High-Level Architecture](./docs/architecture/high_level_architecture.md)
- [API Reference](./docs/api/README.md)
- [Security Strategy](./docs/security/encryption_strategy.md)
- [Deployment Guide](./docs/deployment/local_setup.md)

---

## 🛡 Security & Compliance
Citizen Zero is designed with a "Security-by-Design" philosophy.
- **Data-at-Rest**: Encrypted using AES-256.
- **Data-in-Transit**: TLS 1.3 enforced across all service communications.
- **Identity Standards**: Fully compliant with digital identity standards for non-repudiation.

---
*Developed by [stanlley-locke](https://github.com/stanlley-locke)*
