from twyla.raml import RamlSpecification

BASIC_RAML = """
#%RAML 1.0
---
title: Awesome API
baseUri: http://api.awesome.com/{version}
version: v1

/status:
  get:
    description: Returns the email and tenant of currently logged in user
    responses:
      200:
        body:
          application/json:
            type: object
            properties:
              email:
                type: string
              tenant:
                type: string
"""

def test_load_raml():
    spec = RamlSpecification(BASIC_RAML)
    assert spec.document['title'] == 'Awesome API'

def test_raml_version():
    spec = RamlSpecification(BASIC_RAML)
    assert spec.version == ('RAML', '1.0')


def test_endpoint_available():
    spec = RamlSpecification(BASIC_RAML)
    assert len(spec.endpoints) == 1
    assert '/status' in spec.endpoints

def test_endpoint_attributes():
    spec = RamlSpecification(BASIC_RAML)
    endpoint = spec.endpoints['/status']
    assert len(endpoint.methods) == 1
    assert 'get' in endpoint.methods

def test_method_attributes():
    spec = RamlSpecification(BASIC_RAML)
    method = spec.endpoints['/status'].methods['get']
    assert method.name == 'get'
    assert method.description == "Returns the email and tenant of currently logged in user"
