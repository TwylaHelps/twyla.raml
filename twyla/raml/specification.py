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

METHODS = ['get', 'patch', 'post', 'put', 'delete', 'options', 'head']

class Method:

    def __init__(self, name, section):
        self.name = name
        self.section = section
        self.description = section.get('description', '')
        self.body = self.parse_body(section.get('body', {}))

    def parse_body(self, body_section):
        pass


class Endpoint:

    def __init__(self, path, section):
        self.path = path
        self.section = section
        self.display_name = section.get('displayName', self.path)
        self.methods = {}
        self.load_methods()

    def load_methods(self):
        for key, section in self.section.items():
            if key in METHODS:
                self.methods[key] = Method(key, section)


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
        self.media_type = []
        self.load_media_type()

    def load_documentation(self):
        for doc_section in self.document.get('documentation', []):
            self.documentation[doc_section['title']] = doc_section['content']

    def load_media_type(self):
        if 'mediaType' not in self.document:
            return
        if isinstance(self.document['mediaType'], list):
            self.media_type = self.document['mediaType']
        else:
            self.media_type = [self.document['mediaType']]
        for media_type in self.media_type:
            try:
                mimeparse.parse_mime_type(media_type)
            except ValueError:
                raise RamlSpecificationError("{} is not a valid media type".format(
                    media_type))


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
                self.endpoints[key] = Endpoint(key, section)
