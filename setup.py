# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 14:13:56 2017

@author: cmb11
"""

from setuptools import setup, find_packages

setup(
        name='pycge',
        version='0.1dev',
        python_requires='~=3.6',
        install_requires = [
            'dill>=0.2.7', 
            'pyomo>=5.4.3'
            ],
        packages=find_packages(),
        url='htpps://github.com/juanfung/pycge.git',
        license='',
        description='A python interface for solving CGE models',
        long_description = open('README.md').read(),
        author = 'Juan Fung, Charley Burtwistle',
        author_email = 'juan.fung@nist.gov',
        include_package_data=True
        )
