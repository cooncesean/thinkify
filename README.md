# The Thinkify Python Library
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

```python
>>> from thinkify.reader import ThinkifyReader
>>> reader = ThinkifyReader('/dev/tty.usbmodem1411')

>>> # Get the firmware version on your reader
>>> reader.get_version()
VERSION=2.2.3

>>> # Get a list of nearby tags
>>> tag_list = reader.get_tags()
STARTINVENTORY
TAG=3000E2001021490F02461010ABE9
TAG=3000E2001021490F02460940B41A
STOPINVENTORY=0x0002 0x0031

# Iterate over the tag_list and inspect properties of each `Tag` object
>>> [tag.epc_id for tag in tag_list]
3000E2001021490F02461010ABE9
3000E2001021490F02460940B41A
```

## Notes
This library covers about ~20% of the total functionality provided by the [Thinkify Reader Protocol](http://bit.ly/1dKFJ5x)(TRP) - it basically covers what I currently need. If one feels inclined to add extended functionality, please fork!

Another small side note: Instead of using TRP's `T(x)` command which loops indefinitely looking for tag presence, my current workflow is to handle the looping logic in Python. This is because:

* It's cumbersome to constantly read data from the I/O buffer using pyserial.
* It's difficult to manage the timing of the scan loop on the device itself.

Anyway, it works for my use case -- if someone can think of a cleaner way to handle this, please fork.

## Author
This library is maintained by Sean Coonce and can be found here: https://github.com/cooncesean/thinkify/
