import logging
import json
import urllib

from unicodedata import normalize
from datetime import datetime
from base64 import b64decode, b64encode

log = logging.getLogger(__name__)

class Mojibake:
	def __init__(self, encoding='utf-8', normalizer='NFC', errors='ignore'):
		self.default_encoding   = encoding
		self.default_normalizer = normalizer
		self.default_error_handling = errors

	# Unicode to string, string WILL be returned regardless of type by default
	# If string then it will be decoded then re-encoded
	def encode(self, unicode_data, preserve_type=False):
		try:
			if isinstance(unicode_data, unicode):
				string_data = unicode_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, str):
				string_data = self.decode(unicode_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, int):
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, long):
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, float):
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, datetime):
				string_data = unicode_data.isoformat()
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif isinstance(unicode_data, complex):
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif unicode_data == None:
				string_data = u'None'
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			# Needs testing and validation
			elif isinstance(unicode_data, bytearray):
				string_data = self.decode(unicode_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			# Placeholder for now
			else:
				try:
					string_data = unicode_data.encode(self.default_encoding, self.default_error_handling)

					return string_data

				except Exception as e:
					log.error("Mojibake Error: %s", e)
					raise ValueError("%s is an invalid type for encode()" % (type(unicode_data)))

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# String to unicode; unicode WILL be returned regardless of type by default
	def decode(self, string_data, preserve_type=False):
		try:
			if isinstance(string_data, str):
				unicode_data = normalize(self.default_normalizer, string_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, unicode):
				unicode_data = self.encode(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, int):
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, long):
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, float):
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, datetime):
				unicode_data = string_data.isoformat()
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif isinstance(string_data, complex):
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif string_data == None:
				unicode_data = u'None'

				return unicode_data

			# Needs testing and validation
			elif isinstance(string_data, bytearray):
				unicode_data = normalize(self.default_normalizer, string_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			# Placeholder for now
			else:
				try:
					unicode_data = normalize(self.default_normalizer, string_data.decode(self.default_encoding, self.default_error_handling))

					return unicode_data

				except Exception as e:
					log.error("Mojibake Error: %s", e)
					raise ValueError("%s is an invalid type for decode()" % (type(string_data)))

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a dict to encode all unicode values to strings
	# If string value is observed, it will be decoded then re-encoded
	def dict_encode(self, dict_obj):
		new_dict = dict()

		try:
			if hasattr(dict_obj, 'iteritems'):
				for nKey, nData in dict_obj.iteritems():
					new_nKey = self.encode(nKey)

					if isinstance(nData, dict):
						new_dict[new_nKey] = self.dict_encode(nData)

					elif isinstance(nData, tuple):
						new_dict[new_nKey] = self.tuple_encode(nData)

					elif isinstance(nData, list):
						new_dict[new_nKey] = self.list_encode(nData)

					else:
						new_dict[new_nKey] = self.encode(nData)

			return new_dict
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a dict to decode all string values to unicode
	def dict_decode(self, dict_obj):
		new_dict = dict()

		try:
			if hasattr(dict_obj, 'iteritems'):
				for nKey, nData in dict_obj.iteritems():
					new_nKey = self.decode(nKey)

					if isinstance(nData, dict):
						new_dict[new_nKey] = self.dict_decode(nData)

					elif isinstance(nData, tuple):
						new_dict[new_nKey] = self.tuple_decode(nData)

					elif isinstance(nData, list):
						new_dict[new_nKey] = self.list_decode(nData)

					else:
						new_dict[new_nKey] = self.decode(nData)

			return new_dict
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a list to encode all unicode values to strings
	# If string value is observed, it will be decoded then re-encoded
	def list_encode(self, list_obj):
		new_list = list()

		try:
			if isinstance(list_obj, list):
				for i in range(0, len(list_obj)):
					if hasattr(list_obj[i], 'iteritems'):
						new_list.append(self.dict_encode(list_obj[i]))

					elif isinstance(list_obj[i], list):
						new_list.append(self.list_encode(list_obj[i]))

					elif isinstance(list_obj[i], tuple):
						new_list.append(self.tuple_encode(list_obj[i]))

					else:
						new_list.append(self.encode(list_obj[i]))

			return new_list[::]
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a list to decode all string values to unicode
	def list_decode(self, list_obj):
		new_list = list()

		try:
			if isinstance(list_obj, list):
				for i in range(0, len(list_obj)):
					if hasattr(list_obj[i], 'iteritems'):
						new_list.append(self.dict_decode(list_obj[i]))

					elif isinstance(list_obj[i], list):
						new_list.append(self.list_decode(list_obj[i]))

					elif isinstance(list_obj[i], tuple):
						new_list.append(self.tuple_decode(list_obj[i]))

					else:
						new_list.append(self.decode(list_obj[i]))

			return new_list[::]
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a tuple to decode all unicode values to strings
	# If string value is observed, it will be decoded then re-encoded
	def tuple_encode(self, tuple_obj):
		# Because a tuple is immutable, we have to create a new list
		# and append the tuple data to it after modification then 
		# add it to the new tuple
		new_list  = list()

		try:
			if isinstance(tuple_obj, tuple):
				for i in range(0, len(tuple_obj)):
					if hasattr(tuple_obj[i], 'iteritems'):
						new_list.append(self.dict_encode(tuple_obj[i]))

					elif isinstance(tuple_obj[i], list):
						new_list.append(self.list_encode(tuple_obj[i]))

					elif isinstance(tuple_obj[i], tuple):
						new_list.append(self.tuple_encode(tuple_obj[i]))

					else:
						new_list.append(self.encode(tuple_obj[i]))

				new_tuple = tuple(new_list)
				return new_tuple

			else:
				return tuple_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a tuple to decode all string values to unicode
	def tuple_decode(self, tuple_obj):
		# Because a tuple is immutable, we have to create a new list
		# and append the tuple data to it after modification then 
		# add it to the new tuple
		new_list  = list()

		try:
			if isinstance(tuple_obj, tuple):
				for i in range(0, len(tuple_obj)):
					if hasattr(tuple_obj[i], 'iteritems'):
						new_list.append(self.dict_decode(tuple_obj[i]))

					elif isinstance(tuple_obj[i], list):
						new_list.append(self.list_decode(tuple_obj[i]))

					elif isinstance(tuple_obj[i], tuple):
						new_list.append(self.tuple_decode(tuple_obj[i]))

					else:
						new_list.append(self.decode(tuple_obj[i]))

				new_tuple = tuple(new_list)
				return new_tuple

			else:
				return tuple_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Serializes dict to string using json.dumps AFTER dict_encoding the dictionary
	def dict_to_string(self, dict_obj):
		assert isinstance(dict_obj, dict)

		dict_obj = self.dict_encode(dict_obj)
		serialized_dict = json.dumps(dict_obj)

		return serialized_dict

	# deserializes string to dict object using json.loads AFTER encoding the string
	def string_to_dict(self, serialized_dict):
		assert isinstance(dict_obj, str) or isinstance(dict_obj, unicode)

		serialized_dict = self.encode(serialized_dict)
		dict_obj = json.loads(serialized_dict)

		return dict_obj

	# returns url decoded STRING
	def decode_url(self, string_data):
		try:
			if isinstance(dict_obj, str) or isinstance(dict_obj, unicode):
				string_data    = self.encode(string_data)
				encoded_string = urllib.unquote_plus(string_data)

				return self.encode(encoded_string)

			else:
				raise ValueError('decode_url takes a value of type "str" or "unicode"')

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# returns url encoded STRING
	def encode_url(self, string_data):
		try:
			if isinstance(dict_obj, str) or isinstance(dict_obj, unicode):
				string_data    = self.encode(string_data)
				encoded_string = urllib.quote_plus(string_data)

				return self.encode(encoded_string)

			else:
				raise ValueError('encode_url takes a value of type "str" or "unicode"')

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Returns base64 encoded string
	def b64_encode(self, b64_data):
		try:
			b64_data = self.encode(b64_data)

			return b64encode(b64_data)

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Returns base64 decoded string
	def b64_decode(self, b64_data):
		try:
			b64_data = self.encode(b64_data)

			# Ensure correct padding
			b64_data += "=" * ((4 - len(b64_data) % 4) % 4)

			return b64decode(b64_data)

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise
