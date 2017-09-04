from twyla.raml.specification import Method, APIProperties

def test_name():
    method = Method('get', {}, APIProperties({'title': 'Test'}))
    assert method.name == 'get'

def test_description():
    method = Method('get', {'description': 'Haha'}, APIProperties({'title': 'Test'}))
    assert method.description == 'Haha'

def test_no_description():
    method = Method('get', {}, APIProperties({'title': 'Test'}))
    assert method.description == ''

def test_request_body():
    method = Method('get', {'body': {'application/json': {'type': 'object'}}},
                    APIProperties({'title': 'Test'}))
    assert len(method.body_by_media_type) == 1
    assert 'application/json' in method.body_by_media_type
