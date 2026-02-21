# Citizen Zero: High-Level Architecture

This document outlines the architectural principles and service distribution of the Citizen Zero ecosystem.

## 1. Design Philosophy
Citizen Zero follows a microservices architecture designed for high throughput, data integrity, and strict privacy. The system is divided into three layers:
- **Presentation Layer**: React Web portals, Flutter mobile apps, and PyQt6 desktop consoles.
- **Service Layer**: Independent Django services handling specific domain logic (Identity, Biometrics, Verification).
- **Data Layer**: Specialized databases for transactional data (PostgreSQL), biometric templates (Vector databases/Encrypted storage), and caching (Redis).

## 2. Component Overview

### 2.1 Backend Services
Each service is isolated and communicates via RESTful APIs and asynchronous message queues (Celery/Redis).

- **Identity (ID) Service**: 
  - Central repository for digital identity lifecycle.
  - Generates ISO 18013-5 compliant mDL records.
  - Provides PDF generation for National IDs, Passports, and Birth Certificates.
- **Biometric Service**:
  - Performs 1:1 and 1:N matching for face and fingerprints.
  - Implements liveness detection to prevent deepfake injection.
- **Verification Service**:
  - Handles the validation of digital credentials.
  - Implements Zero-Knowledge Proof (ZKP) protocols to verify age or citizenship without data leakage.
- **Monitor Service**:
  - Acts as an observability hub, tracking service health and network topology.

### 2.2 Frontend Applications
- **Admin Dashboard (Vite/React)**: The primary interface for government officials to manage citizen records and enrollment workflows.
- **Citizen Wallet (Flutter)**: A secure mobile vault for citizens to hold and present their digital IDs.
- **Verifier App (Flutter)**: A lightweight tool for agents (police, banks) to verify presented credentials offline or online.
- **Super Admin (PyQt6)**: A high-security desktop application for system-wide configuration and hardware management (e.g., HSM setup).

## 3. Communication Patterns
- **Synchronous**: REST APIs are used for real-time lookups and simple CRUD operations.
- **Asynchronous**: Long-running biometric processing tasks are offloaded to Celery workers to maintain UI responsiveness.
- **Standards-Based**: Digital credentials are encapsulated in CBOR (Concise Binary Object Representation) and signed using COSE (CBOR Object Signing and Encryption).

## 4. Security Infrastructure
- **Identity Provider (IdP)**: Integrated OAuth2/OpenID Connect flow for administrative access.
- **Hardware Security Modules (HSM)**: Keys for signing digital credentials are stored in HSMs to prevent extraction.
- **End-to-End Encryption**: All sensitive citizen data is encrypted at the application layer before reaching the database.
