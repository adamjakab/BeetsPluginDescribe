#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 3/21/20, 11:27 AM
#  License: See LICENSE.txt

import pathlib
from setuptools import setup
from distutils.util import convert_path

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

main_ns = {}
ver_path = convert_path('beetsplug/describe/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

# Setup
setup(
    name='beets-describe',
    version=main_ns['__version__'],
    description='A beets plugin that describes attributes in depth',
    author='Adam Jakab',
    author_email='adam@jakab.pro',
    url='https://github.com/adamjakab/BeetsPluginDescribe',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    platforms='ALL',

    include_package_data=True,
    test_suite='test',
    packages=['beetsplug.describe'],

    python_requires='>=3.6',

    install_requires=[
        'beets>=1.4.9',
        'numpy',
        'pandas',
        'termtables',
        'termplotlib',
    ],

    tests_require=[
        'pytest', 'nose', 'coverage',
        'mock', 'six', 'yaml',
    ],

    # Extras needed during testing
    extras_require={
        'tests': [],
    },

    classifiers=[
        'Topic :: Multimedia :: Sound/Audio',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
