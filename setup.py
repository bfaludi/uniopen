
from setuptools import setup, find_packages
import sys, os

version = '1.0'

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
        'paramiko'
    ],
    test_suite = "uniopen.tests",
    url = 'http://bfaludi.com'
)