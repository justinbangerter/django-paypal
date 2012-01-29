# -*- coding: utf-8 -*-
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from paypal import VERSION

try:
    README = open('README.md').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = None

setup(
    name = 'django-paypal',
    version = VERSION,
    description = 'description',
    long_description = README,
    install_requires = REQUIREMENTS,
    author = 'John Boxall',
    author_email = 'john@handimobility.ca',
    maintainer="David Cramer",
    maintainer_email="dcramer@gmail.com",
    url = 'https://github.com/awarepixel/django-paypal',
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)