from distutils.core import setup

setup(
    name='thinkify',
    description='A Python wrapper for the Thinkify Reader Protocol.',
    version='0.1.1',
    author='Sean Coonce',
    author_email='cooncesean@gmail.com',
    packages=['thinkify',],
    url='https://github.com/cooncesean/thinkify',
    license='LICENSE.txt',
    long_description=open('README.rst').read(),
    install_requires=[
    	'pyserial>=2.6',
	],
)
