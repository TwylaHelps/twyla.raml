from twyla.raml import Endpoint

def test_display_name_not_specified():
    ep = Endpoint('/status', {'get': {}})
    assert ep.display_name == '/status'
