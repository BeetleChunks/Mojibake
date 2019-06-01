Mojibake
--------

Installation::

	$ git clone https://github.com/BeetleChunks/Mojibake.git
	$ cd Mojibake
	$ python setup.py install

To use, simply do::

	>>> from mojibake import Mojibake
	>>>
	>>> moji = Mojibake()
	>>>
	>>> my_string  = moji.encode(u'Some unicode data')
	>>> my_unicode = moji.decode('Some string data')

Here is a list of available methods::

	encode()
	decode()
	dict_encode()
	dict_decode()
	list_encode()
	list_decode()
	tuple_encode
	tuple_decode
	dict_to_string()
	string_to_dict()
	decode_url()
	encode_url()
