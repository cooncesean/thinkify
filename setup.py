from distutils.core import setup

setup(
    name='thinkify',
    description='A Python wrapper for the Thinkify Reader Protocol.',
    version='0.2.2',
    author='Sean Coonce',
    author_email='cooncesean@gmail.com',
    packages=['thinkify',],
    url='https://github.com/cooncesean/thinkify',
    license='LICENSE.txt',
    long_description='More info can be found at: http://github.com/cooncesean/thinkify',
    install_requires=[
    	'pyserial>=2.6',
	],
)
