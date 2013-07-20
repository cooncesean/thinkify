import os

from distutils.core import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = f.read()
f.close()

setup(
    name='thinkify',
    description='A Python wrapper for the Thinkify Reader Protocol.',
    version='0.1.3',
    author='Sean Coonce',
    author_email='cooncesean@gmail.com',
    packages=['thinkify',],
    url='https://github.com/cooncesean/thinkify',
    license='LICENSE.txt',
    long_description=long_description,
    install_requires=[
    	'pyserial>=2.6',
	],
)
