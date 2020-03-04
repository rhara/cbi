import os
from setuptools import setup, find_packages

setup(
    name='cbi',
    version='0.1.5',
    description='ProDy-OpenBabel-RDKit triad',
    author='Ryuichiro Hara',
    author_email='hara.ryuichiro@gmail.com',
    url='https://github.com/rhara/cbi',
    license='no license',
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'cbi_rmsd = cbi.bin.cbi_rmsd:main',
            'cbi_dock = cbi.bin.cbi_dock:main',
            'cbi_fixprotein = cbi.bin.cbi_fixprotein:main',
            'cbi_prep = cbi.bin.cbi_prep:main',
        ]
    }
)
