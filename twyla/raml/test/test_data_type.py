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
