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


class RamlSpecification:

    def __init__(self, body):
        self.version = parse_version(body) or DEFAULT_VERSION
        self.document = yaml.load(body)
