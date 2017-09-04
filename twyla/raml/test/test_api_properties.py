import pytest

from twyla.raml import RamlSpecificationError
from twyla.raml.specification import APIProperties

def test_title_required():
    """Title is the only thing required. Make sure it's there"""
    with pytest.raises(RamlSpecificationError) as exception_info:
        APIProperties({'baseUri': 'http://blah.com'})
    message = exception_info.value.args[0]
    assert message == 'Please provide a title for your API'


def test_media_type():
    props = APIProperties({'title': 'Test', 'mediaType': 'application/json'})
    assert props.media_type == ['application/json']


def test_no_media_type():
    props = APIProperties({'title': 'Test'})
    assert props.media_type == []


def test_invalid_media_type():
    with pytest.raises(RamlSpecificationError) as exception_info:
        props = APIProperties({'title': 'Test', 'mediaType': 'blah'})
    message = exception_info.value.args[0]
    assert message == 'blah is not a valid media type'


def test_base_uri():
    props = APIProperties({'title': 'Test', 'baseUri': 'http://blah.com'})
    assert props.base_uri == 'http://blah.com'

def test_no_base_uri():
    props = APIProperties({'title': 'Test'})
    assert props.base_uri == ''
