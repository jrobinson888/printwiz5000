from setuptools import find_packages, setup

from print_wiz import __version__

setup(
    name='print_wiz',
    version=__version__,
    description='Printer Controler Example',
    author='Joe Robinson',
    author_email='joe.h.robinson.ucla@gmail.com',
    url='https://github.com/jrobinson888/printwiz5000',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ]
)
