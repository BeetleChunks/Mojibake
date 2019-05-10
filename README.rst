Mojibake
--------

To use, simply do::

	>>> from mojibake import Mojibake
	>>>
	>>> moji = Mojibake()
	>>>
	>>> my_string  = moji.encode(u'Some unicode data')
	>>> my_unicode = moji.decode('Some string data')