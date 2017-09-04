from itertools import takewhile

import yaml
import mimeparse
from parse import parse

VERSION_PATTERN = '#%RAML {version}'
DEFAULT_VERSION = ('RAML', '1.0')

class RamlSpecificationError(Exception):
    pass

def parse_version(body):
    comment_lines = takewhile(lambda x: x.startswith('#'), body.split())
    for line in comment_lines:
        parse_result = parse(VERSION_PATTERN, line)
        if parse_result is None:
            continue
        return ('RAML', parse_result['version'])
    return None

def parse_media_type(media_type_string: str):
    try:
        return mimeparse.parse_mime_type(media_type_string)
    except ValueError:
        return None

METHODS = ['get', 'patch', 'post', 'put', 'delete', 'options', 'head']


class DataType:

    def __init__(self, data_spec):
        self.data_spec = data_spec


class APIProperties:

    def __init__(self, document):
        self.document = document
        try:
            self.title = self.document['title']
        except KeyError:
            raise RamlSpecificationError('Please provide a title for your API')
        self.base_uri = self.document.get('baseUri', '')
        self.documentation = {}
        self.load_documentation()
        self.media_types = []
        self.load_media_types()

    def load_documentation(self):
        for doc_section in self.document.get('documentation', []):
            self.documentation[doc_section['title']] = doc_section['content']

    def load_media_types(self):
        if 'mediaType' not in self.document:
            return
        if isinstance(self.document['mediaType'], list):
            self.media_types = self.document['mediaType']
        else:
            self.media_types = [self.document['mediaType']]
        for media_type in self.media_types:
            if parse_media_type(media_type) is None:
                raise RamlSpecificationError("{} is not a valid media type".format(
                    media_type))


class Method:

    def __init__(self, name: str, section: dict, properties: APIProperties):
        self.name = name
        self.section = section
        self.description = section.get('description', '')
        self.parse_body(section.get('body', {}))


    def parse_body(self, body_section):
        self.body_by_media_type = {}
        if all(parse_media_type(key) for key in body_section.keys()):
            for media_type, section in body_section.items():
                self.body_by_media_type[media_type] = DataType(section)
        else:
            data_type = DataType(body_section)
            for media_type in properties.media_types:
                self.body_by_media_type[media_type] = data_type
            # It should be a type declaration



class Endpoint:

    def __init__(self, path, section, properties):
        self.path = path
        self.section = section
        self.properties = properties
        self.display_name = section.get('displayName', self.path)
        self.methods = {}
        self.load_methods()


    def load_methods(self):
        for key, section in self.section.items():
            if key in METHODS:
                self.methods[key] = Method(key, section, self.properties)



class RamlSpecification:

    def __init__(self, body):
        self.version = parse_version(body) or DEFAULT_VERSION
        self.document = yaml.load(body)
        self.properties = APIProperties(self.document)
        self.endpoints = {}
        self.load_endpoints()

    def load_endpoints(self):
        for key, section in self.document.items():
            if key.startswith('/'):
                self.endpoints[key] = Endpoint(key, section, self.properties)
