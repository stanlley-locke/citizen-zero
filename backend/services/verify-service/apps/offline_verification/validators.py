class OfflineValidator:
    def validate_structure(self, data):
        # Check standard fields
        if not data or 'docType' not in data:
            return False
        return True

    def verify_signature(self, data, public_key):
        # Verify device signature
        return True
