from twyla.raml import Endpoint
from twyla.raml.specification import APIProperties


def test_display_name_not_specified():
    ep = Endpoint('/status', {'get': {}}, APIProperties({'title': 'Test'}))
    assert ep.display_name == '/status'
