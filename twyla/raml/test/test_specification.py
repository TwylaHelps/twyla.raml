import pkg_resources
import pytest

from twyla.raml import RamlSpecification

@pytest.fixture
def raml_file_content():
    path = pkg_resources.resource_filename('twyla.raml.test', 'data/sample-spec.raml')
    with open(path, 'r') as raml_file:
        content = raml_file.read()
    return content

def test_load_raml(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    assert spec.document['title'] == 'Awesome API'

def test_raml_version(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    assert spec.version == ('RAML', '1.0')

def test_base_uri(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    assert spec.base_uri == 'http://api.awesome.com/v1'

def test_documentation(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    assert len(spec.documentation) == 1
    assert spec.documentation['Home'].startswith(
        'Welcome to the Awesome API documentation')

def test_endpoint_available(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    assert len(spec.endpoints) == 1
    assert '/status' in spec.endpoints

def test_endpoint_attributes(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    endpoint = spec.endpoints['/status']
    assert len(endpoint.methods) == 1
    assert 'get' in endpoint.methods

def test_method_attributes(raml_file_content):
    spec = RamlSpecification(raml_file_content)
    method = spec.endpoints['/status'].methods['get']
    assert method.name == 'get'
    assert method.description == "Returns the email and tenant of currently logged in user"
