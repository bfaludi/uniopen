
from setuptools import setup, find_packages
import sys, os

version = '1.0.2'

setup(
    name = 'uniopen',
    version = version,
    description = "Universal File Opener",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    author = 'Bence Faludi',
    author_email = 'bence@ozmo.hu',
    license = 'GPL',
    install_requires = [
        'sqlalchemy',
        'paramiko',
        'smart_open',
        'sqlalchemy-redshift',
    ],
    test_suite = "uniopen.tests",
    url = 'http://bfaludi.com'
)
