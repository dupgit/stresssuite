#!/usr/bin/env python

from distutils.core import setup

import os

# README description (if any)
ldesc = open(os.path.join(os.path.dirname(__file__), 'README')).read()

# A setup call with some arguments
setup(
    # Final module name
    name = 'stresssuite',

    version = '0.0.1',

    # Short descriptin
    description = ('Stress suites to stress your Filesystem, your CPU, ....'),

    # Longer one (here From the README file)
    long_description = ldesc,

    keywords = 'stress load tests benchmark filesystem cpu',

    author = 'Olivier DELHOMME',

    author_email = 'olivier.delhomme@free.fr',

    license = 'GPL v2 or later',

    packages = ['stresssuite'],
    package_dir = {'stresssuite': 'stresssuite'},

    url = 'https://gna.org/projects/gstressfs/',

    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers for a list
    # of classifiers
    classifiers = [
        'Programming Language :: Python :: 2.6',
        'Topic :: System',
        'Topic :: System :: Benchmark',
        'Topic :: System :: Filesystems'
        'Topic :: System :: Systems Administration'
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)'
        'Operating System :: Unix',
        'Programming Language :: Python',
        ],
)
