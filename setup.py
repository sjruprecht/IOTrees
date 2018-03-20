#!/usr/bin/env python

from setuptools import find_packages, setup


setup(
    name='iotrees',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'detect=iotrees.detect:main',
            'eab_find=iotrees.eab_find:main',
        ]
    }
)
