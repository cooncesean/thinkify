from distutils.core import setup

install_requires = [
    'pyserial>=2.6',
]

setup(
    name='Thinkify',
    description='A Python wrapper for the Thinkify Reader Protocol.'
    version='0.1',
    packages=['thinkify',],
    url='https://github.com/cooncesean/thinkify',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=install_requires,
)
