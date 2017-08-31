from setuptools import setup

dependencies = ['PyYAML>3', 'parse']

setup(
    name="twyla-raml",
    version="0.1",
    author="Twyla Devs",
    author_email="dev@twylahelps.com",
    description=("Twyla Raml Verifier"),
    install_requires=dependencies,
    extras_require={
        'test': ['pytest'],
    },
    packages=["twyla.raml"],
    entry_points={
        'console_scripts': [
            'twyla-raml = twyla.raml.main:load',
        ]
    },
    url="https://bitbucket.org/twyla/twyla.raml",
)
