# -*- coding: utf-8 -*-

import codecs

from setuptools import setup

long_description = codecs.open("README.rst", "r", "utf-8").read()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Framework :: Django',
]

import dbag
setup(
    name='dbag',
    version=dbag.__version__,
    description=dbag.__doc__,
    author=dbag.__author__,
    author_email=dbag.__contact__,
    url=dbag.__homepage__,
    long_description=long_description,
    packages=['dbag'],
    license='BSD',
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'nexus>=0.1.7',
        'django-jsonfield',
        'Django>=1.1',
    ],
    test_suite='runtests.runtests',
    include_package_data=True,
)
