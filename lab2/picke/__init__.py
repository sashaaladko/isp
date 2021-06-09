from ..json_serializer import JsonSerializer

class PickleSerializer:
    
    def __init__(self):
        self.s = JsonSerializer()

    def loads(self, bin_string):
        return self.s.loads(self.from_hex(bin_string))

    def dumps(self, obj):
        return self.to_hex(self.s.dumps(obj))

    def load(self, fp):
        fp.seek(0)
        bin_string = fp.read()

        return self.loads(bin_string)  

    def dump(self, obj, fp):
        bin_string = self.dumps(obj)
        
        fp.write(bin_string)
        fp.flush()

    def __str__(self):
        return 'Pickle serializer'

    def to_hex(self, s):
        return r"\x".join("{:02x}".format(c) for c in s.encode())

    def from_hex(self, hex):
        return r"".join("{}".format(chr(int(c, 16))) for c in hex.split(r'\x'))