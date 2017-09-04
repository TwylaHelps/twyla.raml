from twyla.raml.data_types import DataType, StringType

def test_creates_subset_by_key():
    string_type = DataType.from_spec({'type': 'string'})
    assert isinstance(string_type, StringType)
