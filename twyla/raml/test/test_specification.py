from twyla.raml import RamlSpecification

BASIC_RAML = """
#%RAML 1.0
---
title: Awesome API
baseUri: http://api.awesome.com/{version}
version: v1
/status:
  get:
    description: returns the email and tenant of currently logged in user
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
