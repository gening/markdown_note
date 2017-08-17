"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
"""

# Always prefer setuptools over distutils
# To use a consistent encoding
from codecs import open
from os import path

from setuptools import setup, find_packages

NAME = 'markdown_note'
DESCRIPTION = 'Command Line on Markdown Note.'
AUTHOR = 'GE Ning'
AUTHOR_EMAIL = 'benjaminzge@gmail.com'
URL = 'https://github.com/gening/markdown_note'
PACKAGE = 'markdown_note'
LICENSE = __import__(PACKAGE).__license__
VERSION = __import__(PACKAGE).__version__

here = path.abspath(path.dirname(__file__))


# Get the long description from the README file
def get_long_description(filename='README.md'):
    file_path = path.join(here, filename)
    if path.exists(file_path) and path.isfile(file_path):
        with open(path.join(here, filename), encoding='utf-8') as f:
            return f.read()
    raise RuntimeError('Unable to find README file')


setup_args = dict(
    name=NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=VERSION,

    description=DESCRIPTION,
    long_description=get_long_description(),

    # The project's main homepage.
    url=URL,

    # Author details
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,

    # Choose your license
    license=LICENSE,

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords='markdown',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests']),  # 'contrib', 'docs', 'tests'

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #    'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # scripts=['bin/note'],
    entry_points={
        'console_scripts': [
            'note=markdown_note.note:main',
            'note-rm=markdown_note.note_remove:main',
            'note-cp=markdown_note.note_copy:main',
            'note-mv=markdown_note.note_move:main',
            'note-offline=markdown_note.note_offline:main',
            'note-mkdir=markdown_note.note_mkdir:main',
            'note-rmdir=markdown_note.note_rmdir:main',
            'note-opendir=markdown_note.note_opendir:main',
        ],
    },
)

# Optimize calling command line script for Linux and macOS
# import platform
# if platform.system() in ['Linux', 'Darwin']:
#     del setup_args['entry_points']
# else:
#     del setup_args['scripts']

setup(**setup_args)
