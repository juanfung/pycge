# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 14:13:56 2017

@author: cmb11
"""

from distutils.core import setup

setup(
        name='PyCGE',
        version='0.1dev',
        packages=['pycge','tests','pycge/examples'],
        url='',
        license='',
        description='',
        long_description = open('README.txt').read(),
        author = 'Juan Fung, Charley Burtwistle',
        author_email = 'juan.fung@nist.gov',
        include_package_data=True
        )