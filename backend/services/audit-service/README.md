# Audit Service Design
This service will implement the "Immutable audit trail with cryptographic chaining (SHA-3 hashes)".
## Core Concept
Each audit log entry will contain:
- `timestamp`
- `action`
- `actor`
- `metadata` (JSON)
- `previous_hash` (Hash of the previous log entry)
- `hash` (SHA-3 hash of this entry + previous_hash)

This creates a lightweight blockchain structure where history cannot be altered without breaking the chain.
