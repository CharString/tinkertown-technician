
# -*- coding: utf-8 -*-
import codecs

from setuptools import setup

with codecs.open('README.md', encoding="utf-8") as fp:
    long_description = fp.read()
INSTALL_REQUIRES = [
    'requests',
    'typer',
    'watchdog',
]
ENTRY_POINTS = {
    'console_scripts': [
        'ttt = tinkertown.__main__:app',
    ],
}

setup_kwargs = {
    'name': 'tinkertown-technician',
    'version': '0.1.0',
    'description': 'Tinkertown Technician -- Battlecry: Fix your Heartstone Deck Tracker',
    'long_description': long_description,
    'license': 'GPL-3.0-or-later',
    'author': '',
    'author_email': 'Chris Wesseling <chris.wesseling@xs4all.nl>',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'packages': [
        'tinkertown',
    ],
    'package_data': {'': ['*']},
    'long_description_content_type': 'text/markdown',
    'classifiers': [
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.8',
    'entry_points': ENTRY_POINTS,

}


setup(**setup_kwargs)
