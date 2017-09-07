TYPES = {}

def for_type(type_name):
    def deco(cls):
        TYPES[type_name] = cls
        return cls
    return deco


class DataType:

    def __init__(self, spec):
        self.required = spec.pop('required', True)
        self.spec = spec
        self.parse_spec()

    @classmethod
    def from_spec(cls, spec):
        return TYPES[spec['type']](spec)

    def parse_spec(self):
        raise NotImplementedError()


class ValidationError:
    def __init__(self, field_name, error_message):
        self.field_name = field_name
        self.error_message = error_message

    def __repr__(self):
        return '<ValidationError field: {} error_message: {}>'.format(
            self.field_name, self.error_message)

    def update_field_path(self, field_prefix):
        if not self.field_name:
            self.field_name = field_prefix
        else:
            self.field_name = '.'.join([field_prefix, self.field_name])


@for_type('string')
class StringType(DataType):

    def parse_spec(self):
        pass

    def validate(self, value):
        if not isinstance(value, str):
            return [ValidationError('', 'Value is of type {}, string expected'.format(
                type(value).__name__))]


@for_type('object')
class ObjectType(DataType):

    def parse_spec(self):
        self.properties = {}
        properties = self.spec.get('properties', [])
        for key in properties:
            self.properties[key] = DataType.from_spec(properties[key])

    def validate(self, data):
        errors = []
        for key, item in self.properties.items():
            if key not in data:
                if item.required:
                    errors.append(ValidationError(key, 'Field is required'))
                continue
            item_errors = item.validate(data[key])
            if item_errors:
                for error in item_errors:
                    error.update_field_path(key)
                errors.extend(item_errors)
        return errors
