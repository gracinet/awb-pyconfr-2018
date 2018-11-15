# -*- coding: utf-8 -*-
# This file is a part of Kalkol project
#
#    Copyright (C) 2018 Georges Racinet <gracinet@anybox.fr>
#
# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file,You can
# obtain one at http://mozilla.org/MPL/2.0/.
from setuptools import setup, find_packages
import os

version = '0.0.1'


here = os.path.abspath(os.path.dirname(__file__))

requirements = [
    'anyblok_wms_base>=0.8.0.dev0',
]

description = "Support for live demo and example at pycon.fr conference"

setup(
    name='wms-demo',
    version=version,
    description=description,
    long_description=description,
    author="Georges Racinet",
    author_email='gracinet@anybox.fr',
    packages=find_packages(),
    entry_points={
        'bloks': [
            'pyconfr-2018=wms_demo:WmsDemo',
        ],
        'console_scripts': [
            'add_data=wms_demo:add',
            'translate_en=wms_demo:translate_en',
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='stock logistics wms demo',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
#    test_suite='tests',
#    tests_require=requirements + ['nose'],
)
