import os
from setuptools import setup, find_packages

setup(
    name='bindlib',
    version='0.1.3',
    description='ProDy-OpenBabel-RDKit triad',
    author='Ryuichiro Hara',
    author_email='hara.ryuichiro@gmail.com',
    url='https://github.com/rhara/bindlib',
    license='no license',
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
        ]
    }
)
