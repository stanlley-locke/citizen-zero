# Security & Encryption Strategy

Citizen Zero employs a multi-layered security model to protect the most sensitive national asset: citizen identity.

## 1. Cryptographic Identity
All digital IDs are encapsulated using **ISO 18013-5 (mDL)** standards. 
- **Encoding**: Concise Binary Object Representation (CBOR).
- **Signing**: CBOR Object Signing and Encryption (COSE) with ECDSA (Curve P-256).

## 2. Privacy Preservation (Zero-Knowledge Proofs)
We utilize **ZKP (Zero-Knowledge Proofs)** to enable "Selective Disclosure".
- **Use Case**: A citizen can prove they are over 18 for entry into a restricted venue without revealing their full name or date of birth.
- **Protocol**: Implementation based on SNARKs/Groth16 for efficient proof generation on mobile devices and fast verification on servers.

## 3. Biometric Security
- **Template Protection**: Biometric data is never stored as raw images. Features are extracted into high-dimensional embeddings (hashes) and encrypted.
- **Liveness Enforcement**: All biometric interactions require a liveness check to prevent presentation attacks (printed photos, video playbacks, deepfakes).

## 4. Administrative Security
- **Role-Based Access Control (RBAC)**: Fine-grained permissions across the Admin Dashboard, Employer Portal, and Super Admin console.
- **Audit Trails**: Every administrative action (view, edit, delete, issue) is logged in an immutable audit trail with an associated user session and timestamp.

## 5. Transport Security
- **TLS 1.3**: Mandatory for all service-to-service and client-to-service communication.
- **API Security**: Request signing and HMAC verification for all backend-to-backend calls.
