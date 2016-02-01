#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import warnings
from setuptools import setup, Extension
from Cython.Distutils import build_ext

dist_dir = os.path.dirname(os.path.abspath(__file__))
os.system("gunzip -kf %s/irtrans/models/* 2> /dev/null" %dist_dir)

try:
    import py2exe
except ImportError:
    if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        print("Cannot import py2exe", file=sys.stderr)
        exit(1)

py2exe_options = {
    "bundle_files": 1,
    "compressed": 1,
    "optimize": 2,
    "dist_dir": '.',
    "dll_excludes": ['w9xpopen.exe'],
}

py2exe_console = [{
    "script": "./irtrans/__main__.py",
    "dest_base": "irtrans",
}]

py2exe_params = {
    'console': py2exe_console,
    'options': {"py2exe": py2exe_options},
    'zipfile': None
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
    params = py2exe_params
else:
    files_spec = [
        ('share/doc/irtrans', ['README.rst'])
    ]
    root = os.path.dirname(os.path.abspath(__file__))
    data_files = []
    for dirname, files in files_spec:
        resfiles = []
        for fn in files:
            if not os.path.exists(fn):
                warnings.warn('Skipping file %s since it is not present. Type  make  to build all automatically generated files.' % fn)
            else:
                resfiles.append(fn)
        data_files.append((dirname, resfiles))

    params = {
        'data_files': data_files,
    }
    params['entry_points'] = {'console_scripts': ['irtrans = irtrans:main']}

# Get the version from youtube_dl/version.py without importing the package
exec(compile(open('irtrans/version.py').read(),
             'irtrans/version.py', 'exec'))

setup(
    name = "irtrans",
    version = __version__,
    description="Transliteration Tool: Hindi to Urdu transliterator and vice-versa",
    long_description = open('README.rst', 'rb').read().decode('utf8'),
    keywords = ['Language Transliteration', 'Computational Linguistics', 
		'Indic', 'Roman'],
    author=['Riyaz Ahmad', 'Irshad Ahmad'],
    author_email='irshad.bhat@research.iiit.ac.in',
    maintainer='Irshad Ahmad',
    maintainer_email='irshad.bhat@research.iiit.ac.in',
    license = "MIT",
    url="https://github.com/irshadbhat/irtrans",
    package_dir={"hutrams":"irtrans"},
    packages=['irtrans', 'irtrans._utils', 'irtrans._decode'],
    package_data={'irtrans': ['models/*.npy']},

    classifiers=[
        "Topic :: Indian Languages :: Transliteration",
        "Environment :: Console",
        "License :: Public Domain",
        "Programming Language :: Python :: 2.7"
    ],
    cmdclass={'build_ext': build_ext},
    ext_modules=[
        Extension("irtrans._decode.viterbi", ["irtrans/_decode/viterbi.pyx"]),
    ],
    install_requires=["cython", "numpy", "scipy"],
    #requires=["cython", "numpy", "scipy"],
    **params
)
