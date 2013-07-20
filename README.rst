The Thinkify Python Library
========

This library is a Python wrapper for `Thinkify's <http://www.thinkifyit.com>`_ Thinkify Reader Protocol. It allows developers to issue commands to their RFID readers as well as retreive data from them.

Installation
---------------

To install the Thinkify python library using `pip <https://pypi.python.org/pypi/pip>`_:

.. code-block:: bash

	$ sudo pip install thinkify


or alternatively via easy_install:

.. code-block:: bash

	$ sudo easy_install thinkify


or from source:

.. code-block:: bash

	$ sudo python setup.py install


Usage
---------------

.. code-block:: pycon

	>>> from thinkify.reader import ThinkifyReader
	>>> reader = ThinkifyReader('/dev/tty.usbmodem1411')

	>>> # Get the firmware version on your reader
	>>> reader.get_version()
	VERSION=2.2.3

	>>> # Get a list of nearby tags
	>>> tag_list = reader.get_tags()
	STARTINVENTORY
	TAG=3000E2001021490
	TAG=3000E2001021491
	STOPINVENTORY=0x0002 0x0031

	# Iterate over the tag_list and inspect properties of each `Tag` object
	>>> [tag.epc_id for tag in tag_list]
	3000E2001021490
	3000E2001021491

	# Finding the closest Tag
	>>> tag = reader.get_closest_tag()
	>>> tag.signal_strength
	23.9234987345

Handling Tag Prefixes
^^^^^^^^^^^^^^^^^

A common case is to have a number of similar tags from the same manufacturer with the same prefix on them. To parse this prefix when reading tags, you may optionally pass the prefix as a named arg to the ThinkifyReader.__init__() method like so.

.. code-block:: pycon

	>>> reader = ThinkifyReader('/dev/tty.usbmodem1411', tag_id_prefix='SOME_PREFIX_STRING')
	>>> tag = reader.get_closest_tag()
	>>> tag.epc_id # The full id
	SOME_PREFIX_STRING_000001

	>>> tag.trunc_id
	000001

Notes
---------------

This library covers about ~20% of the total functionality provided by the `Thinkify Reader Protocol <http://bit.ly/1dKFJ5x>`_ (TRP) - it basically covers what I currently need. If one feels inclined to add extended functionality, please fork!

Another small side note: Instead of using TRP's "T(x)" command which loops indefinitely looking for tag presence, my current workflow is to handle the looping logic in Python. This is because:

* It's cumbersome to constantly read data from the I/O buffer using pyserial.
* It's difficult to manage the timing of the scan loop on the device itself.

Anyway, it works for my use case -- if someone can think of a cleaner way to handle this, please fork.

Author
---------------

This library is maintained by Sean Coonce and can be found here: https://github.com/cooncesean/thinkify/
