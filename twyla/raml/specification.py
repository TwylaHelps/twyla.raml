from itertools import takewhile

import yaml
from parse import parse

VERSION_PATTERN = '#%RAML {version}'
DEFAULT_VERSION = ('RAML', '1.0')

def parse_version(body):
    comment_lines = takewhile(lambda x: x.startswith('#'), body.split())
    for line in comment_lines:
        parse_result = parse(VERSION_PATTERN, line)
        if parse_result is None:
            continue
        return ('RAML', parse_result['version'])
    return None

METHODS = ['get', 'post', 'put', 'delete']

class Method:

    def __init__(self, name, section):
        self.name = name
        self.section = section
        self.description = section.get('description', '')


class Endpoint:

    def __init__(self, path, section):
        self.path = path
        self.section = section
        self.methods = {}
        self.load_methods()

    def load_methods(self):
        for key, section in self.section.items():
            if key in METHODS:
                self.methods[key] = Method(key, section)


class RamlSpecification:

    def __init__(self, body):
        self.version = parse_version(body) or DEFAULT_VERSION
        self.document = yaml.load(body)
        self.base_uri = self.document['baseUri']
        self.endpoints = {}
        self.load_endpoints()
        self.documentation = {}
        self.load_documentation()

    def load_endpoints(self):
        for key, section in self.document.items():
            if key.startswith('/'):
                self.endpoints[key] = Endpoint(key, section)


    def load_documentation(self):
        for doc_section in self.document.get('documentation', []):
            self.documentation[doc_section['title']] = doc_section['content']
