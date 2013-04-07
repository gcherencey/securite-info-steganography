#!/usr/bin/env python
from distutils.core import setup

setup(
    name='steganography',
    version='0.1.0',
    author='Gaylord CHERENCEY',
    author_email='gaylord.cherencey@gmail.com',
    packages=['steganography'],
    scripts=['bin/encryption', 'bin/decryption'],
    description='Encryption of a message in a picture',
    long_description=open('README.txt').read()
)