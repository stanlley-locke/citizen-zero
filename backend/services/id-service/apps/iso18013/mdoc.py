class MDoc:
    def __init__(self):
        self.namespaces = {}

    def add_namespace(self, name, items):
        self.namespaces[name] = items

    def to_cbor(self):
        # Stub for ISO 18013-5 mDoc structure
        return {"docType": "org.iso.18013.5.1.mDL", "namespaces": self.namespaces}
