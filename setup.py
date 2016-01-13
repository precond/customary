# coding=utf-8

"""Django-Customary setup module.
See:
https://github.com/precond/django-customary
"""

from __future__ import unicode_literals

from codecs import open
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-customary',
    version='0.0.1.dev4',
    description='Customary Toolbox for Django',
    long_description=long_description,
    url='https://github.com/precond/django-customary',
    author='Juhana Räsänen',
    author_email='juhana.rasanen@precond.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='SME CRM application development Django',
    packages=find_packages(exclude=['testproject']),
    install_requires=['django>=1.8'],
)
