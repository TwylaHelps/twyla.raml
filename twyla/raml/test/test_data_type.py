from twyla.raml.data_types import DataType, StringType

def test_creates_subset_by_key():
    string_type = DataType.from_spec({'type': 'string'})
    assert isinstance(string_type, StringType)


def test_required():
    string_type = DataType.from_spec({'type': 'string', 'required': False})
    assert not string_type.required


def test_required_default_true():
    string_type = DataType.from_spec({'type': 'string'})
    assert string_type.required


def test_object_tree():
    spec = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'email': {'type': 'string',
                      'required': False}
        }
    }
    object_type = DataType.from_spec(spec)
    assert len(object_type.properties.keys()) == 2
    assert isinstance(object_type.properties['name'], StringType)


def test_string_validation():
    validation_errors = StringType({}).validate(0)
    assert len(validation_errors) == 1
    assert validation_errors[0].error_message == 'Value is of type int, string expected'


def test_object_validation():
    spec = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'email': {'type': 'string',
                      'required': False}
        }
    }
    object_type = DataType.from_spec(spec)
    errors = object_type.validate({'name': 'Ulas'})
    assert len(errors) == 0

    errors = object_type.validate({})
    assert len(errors) == 1
    assert errors[0].error_message == 'Field is required'
    assert errors[0].field_name == 'name'


def test_deep_object_errors():
    spec = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'profile': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string',
                              'required': False}
                }}}}
    object_type = DataType.from_spec(spec)
    errors = object_type.validate({'name': 'Ulas', 'profile': {'email': 10}})
    assert len(errors) == 1
    assert errors[0].error_message == 'Value is of type int, string expected'
    assert errors[0].field_name == 'profile.email'
