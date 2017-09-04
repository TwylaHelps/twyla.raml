TYPES = {}

def for_type(type_name):
    def deco(cls):
        TYPES[type_name] = cls
        return cls
    return deco

class DataType:

    def __init__(self, spec):
        self.spec = spec
        self.parse_spec()

    @classmethod
    def from_spec(cls, spec):
        return TYPES[spec['type']](spec)


@for_type('string')
class StringType(DataType):

    def parse_spec(self):
        pass


@for_type('object')
class ObjectType(DataType):

    def parse_spec(self):
        pass
