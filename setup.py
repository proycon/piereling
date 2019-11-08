#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import io
from setuptools import setup


def getreadme():
    for fname in ('README.rst','README.md', 'README'):
        if os.path.exists(fname):
            return io.open(os.path.join(os.path.dirname(__file__), fname),'r',encoding='utf-8').read()
    return ""

setup(
    name = "piereling",
    version = "0.2",
    author = "Maarten van Gompel",
    description = ("Piereling is a webservice and web-application to convert between a variety of document formats, mostly from and to FoLiA XML. It is intended for NLP pipelines."),
    license = "GPL",
    keywords = "webservice nlp computational_linguistics rest folia conversion",
    url = "https://github.com/proycon/piereling", #update this!
    packages=['piereling'],
    long_description=getreadme(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3.4", #3.0, 3.1 and 3.2 are not supported by flask/CLAM
        "Programming Language :: Python :: 3.5", #3.0, 3.1 and 3.2 are not supported by flask/CLAM
        "Programming Language :: Python :: 3.6", #3.0, 3.1 and 3.2 are not supported by flask/CLAM
        "Programming Language :: Python :: 3.7", #3.0, 3.1 and 3.2 are not supported by flask/CLAM
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    package_data = {'piereling':['*.wsgi','*.yml'] },
    include_package_data=True,
    install_requires=['CLAM >= 3.0', 'FoLiA-tools >= 2.2.6']
)
