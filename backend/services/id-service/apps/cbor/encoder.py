import cbor2

class CBOREncoder:
    @staticmethod
    def encode(data):
        return cbor2.dumps(data)

class CBORDecoder:
    @staticmethod
    def decode(data):
        return cbor2.loads(data)
