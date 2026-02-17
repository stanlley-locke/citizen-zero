import hashlib
import json

def hash_data(data):
    """
    Creates a SHA-256 hash of a dictionary or string.
    """
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def sign_data(data, private_key):
    """
    Placeholder for signing data (e.g. using Ed25519 or ECDSA).
    Real implementation would require `cryptography` library keys.
    """
    # Mock signature for MVP
    return f"signature_{hash_data(data)}"
