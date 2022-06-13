#!/usr/bin/env python3

from genericpath import isfile
from setuptools import setup
import os
import sys
from glob import glob
from itertools import chain


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def generate_data_files(appname, data_dirs):
    data_files = []
    for path, dirs, files in chain.from_iterable(os.walk(data_dir) for data_dir in data_dirs):
        install_dir = os.path.join(appname + '/' + path)    
        list_entry = (install_dir, [os.path.join(path, f) for f in files if not f.startswith('.')])
        data_files.append(list_entry)

    return data_files


setup(
    name='locker-myapps',
    version='0.0.3',
    scripts=['bin/myapps'],
    packages=[
        'myapps',
        'startme.mods.myapps'],
    install_requires=[
        'requests',
        'loguru',
        'lightsleep'
        ],
    
    data_files= generate_data_files('locker_myapps', ['_locker_deploy']),

    url='https://github.com/yaroslaff/locker-myapps',
    license='MIT',
    author='Yaroslav Polyakov',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author_email='yaroslaff@gmail.com',
    description='application manager for locker-server',

    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
)
