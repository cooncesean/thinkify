from distutils.core import setup

install_requires = [
    'pyserial>=2.6',
]

setup(
    name='Thinkify',
    description='A Python wrapper for the Thinkify Reader Protocol.',
    version='0.1.0',
    author='Sean Coonce',
    author_email='cooncesean@gmail.com',
    packages=['thinkify',],
    url='https://github.com/cooncesean/thinkify',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=install_requires,
)
