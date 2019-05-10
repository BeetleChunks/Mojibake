import logging
import json
import urllib

from unicodedata import normalize

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
			if type(unicode_data) == unicode:
				string_data = unicode_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif type(unicode_data) == str:
				string_data = self.decode(unicode_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif type(unicode_data) == int:
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif type(unicode_data) == long:
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif type(unicode_data) == float:
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif type(unicode_data) == complex:
				string_data = str(unicode_data)
				string_data = self.decode(string_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			elif unicode_data == None:
				string_data = u'None'
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			# Needs testing and validation
			elif type(unicode_data) == bytearray:
				string_data = self.decode(unicode_data)
				string_data = string_data.encode(self.default_encoding, self.default_error_handling)

				return string_data

			# Placeholder for now
			else:
				raise ValueError("%s is an invalid type for encode()" % (type(unicode_data)))

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# String to unicode; unicode WILL be returned regardless of type by default
	def decode(self, string_data, preserve_type=False):
		try:
			if type(string_data) == str:
				unicode_data = normalize(self.default_normalizer, string_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif type(string_data) == unicode:
				unicode_data = self.encode(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif type(string_data) == int:
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif type(string_data) == long:
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif type(string_data) == float:
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif type(string_data) == complex:
				unicode_data = str(string_data)
				unicode_data = normalize(self.default_normalizer, unicode_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			elif string_data == None:
				unicode_data = u'None'

				return unicode_data

			# Needs testing and validation
			elif type(string_data) == bytearray:
				unicode_data = normalize(self.default_normalizer, string_data.decode(self.default_encoding, self.default_error_handling))

				return unicode_data

			# Placeholder for now
			else:
				raise ValueError("%s is an invalid type for encode()" % (type(string_data)))

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a dict to encode all unicode values to strings
	# If string value is observed, it will be decoded then re-encoded
	def dict_encode(self, dict_obj):
		try:
			if hasattr(dict_obj, 'iteritems'):
				for nKey, nData in dict_obj.iteritems():
					if type(nData) == unicode:
						dict_obj[nKey] = self.encode(nData)

					elif type(nData) == str:
						dict_obj[nKey] = self.encode(nData)

					elif isinstance(nData, dict):
						dict_obj[nKey] = self.dict_encode(nData)
					
					elif isinstance(nData, list):
						for i in range(0, len(nData)):
							nData[i] = self.dict_encode(nData[i])

						dict_obj[nKey] = nData

			else:
				dict_obj = self.encode(dict_obj)

			return dict_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a dict to decode all string values to unicode
	def dict_decode(self, dict_obj):
		try:
			if hasattr(dict_obj, 'iteritems'):
				for nKey, nData in dict_obj.iteritems():
					if type(nData) == unicode:
						dict_obj[nKey] = self.decode(nData)

					elif type(nData) == str:
						dict_obj[nKey] = self.decode(nData)

					elif isinstance(nData, dict):
						dict_obj[nKey] = self.dict_decode(nData)
					
					elif isinstance(nData, list):
						for i in range(0, len(nData)):
							nData[i] = self.dict_decode(nData[i])

						dict_obj[nKey] = nData

			else:
				dict_obj = self.decode(dict_obj)

			return dict_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a list to encode all unicode values to strings
	# If string value is observed, it will be decoded then re-encoded
	def list_encode(self, list_obj):
		try:
			if type(list_obj) == list:
				for i in range(0, len(list_obj)):
					if hasattr(list_obj[i], 'iteritems'):
						list_obj[i] = self.dict_encode(list_obj[i])

					elif type(list_obj[i]) == list:
						list_obj[i] = self.list_encode(list_obj[i])

					else:
						list_obj[i] = self.encode(list_obj[i])

			return list_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Itters a list to decode all string values to unicode
	def list_decode(self, list_obj):
		try:
			if type(list_obj) == list:
				for i in range(0, len(list_obj)):
					if hasattr(list_obj[i], 'iteritems'):
						list_obj[i] = self.dict_decode(list_obj[i])

					elif type(list_obj[i]) == list:
						list_obj[i] = self.list_decode(list_obj[i])

					else:
						list_obj[i] = self.decode(list_obj[i])

			return list_obj
							
		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise

	# Serializes dict to string using json.dumps AFTER dict_encoding the dictionary
	def dict_to_string(self, dict_obj):
		assert type(dict_obj) == dict

		dict_obj = self.dict_encode(dict_obj)
		serialized_dict = json.dumps(dict_obj)

		return serialized_dict

	# deserializes string to dict object using json.loads AFTER encoding the string
	def string_to_dict(self, serialized_dict):
		assert type(serialized_dict) == str or type(serialized_dict) == unicode

		serialized_dict = self.encode(serialized_dict)
		dict_obj = json.loads(serialized_dict)

		return dict_obj

	# returns url decoded STRING
	def decode_url(self, string_data):
		try:
			if type(string_data) == str or type(string_data) == unicode:
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
			if type(string_data) == str or type(string_data) == unicode:
				string_data    = self.encode(string_data)
				encoded_string = urllib.quote_plus(string_data)

				return self.encode(encoded_string)

			else:
				raise ValueError('encode_url takes a value of type "str" or "unicode"')

		except Exception as e:
			log.exception("%s", e, exc_info=True)
			raise
