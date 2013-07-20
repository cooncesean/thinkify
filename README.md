# Thinkify Python Library
This library is a Python wrapper for [Thinkify's](http://www.thinkifyit.com) Thinkify Reader Protocol. It allows developers to issue commands to their RFID readers as well as retreive data from them.

## Installation
To install the Thinkify python library using [pip](https://pypi.python.org/pypi/pip):

```
$ sudo pip install thinkify
```

or alternatively via easy_install:

```
$ sudo easy_install thinkify
```

or from source:

```
$ sudo python setup.py install
```

## Usage

```
>>> from thinkify.reader import ThinkifyReader
>>> reader = ThinkifyReader('/dev/tty.usbmodem1411')

>>> # Get the firmware version on your reader
>>> reader.get_version()
VERSION=2.2.3

>>> # Get a list of nearby tags
>>> tag_list = reader.get_tags()
>>> [tag.epc_id for tag in tag_list]
<epc_id_1>
<epc_id_2>
....
```

## Author
This library is maintained by Sean Coonce and can be found here: https://github.com/cooncesean/thinkify/