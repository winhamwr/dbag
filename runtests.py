#!/usr/bin/env python

import sys
from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'sqlite3',
            },
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.contenttypes',

            'dbag',

            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        TEMPLATE_DEBUG=True,
        TEMPLATE_STRING_IF_INVALID = "INVALID_TEMPLATE_VARIABLE",
    )

from django.test.simple import run_tests

def runtests(*test_args):
    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(failures)

if __name__ == '__main__':
    runtests(*sys.argv[1:])
