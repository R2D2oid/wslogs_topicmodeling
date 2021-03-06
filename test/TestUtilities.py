import sys
sys.path.append ('.')
import unittest
import lib.utilities as utils
from model.apachelogschema import ApacheLogSchemaRaw, ApacheLog

class TestUtilities (unittest.TestCase):
	def test_flatten_nested_dct(self):
		dct = {'ip':'127.0.0.1', 'bytes_out' : '100', 'geo' : {'lat' : '43.64', 'lon' : '79.38', 'loc' : {'country' : 'CA', 'city' : 'Toronto'}}}
		actual = utils.flatten_nested_dct(dct)
		expected = {'ip': '127.0.0.1', 'bytes_out': '100', 'geo_lat': '43.64', 'geo_lon': '79.38', 'geo_loc_country': 'CA', 'geo_loc_city': 'Toronto'}
		self.assertEqual (actual , expected)

	def test_flatten_nested_dct_null(self):
		dct = {}
		actual = utils.flatten_nested_dct(dct)
		expected = {}
		self.assertEqual (actual , expected)
	
	def test_configloader (self):
		configpath = 'config.cfg.template'
		config = utils.configloader (configpath)
		actual = config['samplesection']['var']
		expected = 'value' 
		self.assertEqual (actual , expected)

	def test_dataloader (self):
		datafile = 'data/wslog.dat.template'
		data = utils.dataloader (datafile, ApacheLogSchemaRaw, ' ')
		actual = data[0]
		expected = {'ip': '198.0.200.105', 
				'user_ident': '-',
				'user_http': '-', 
				'ts': '[14/Jan/2014:09:36:50', 
				'ms': '-0800]', 
				'request': 'GET /svds.com/rockandroll HTTP/1.1', 
				'response_code': '301', 
				'bytes_out': '241', 
				'referrer': '-',
				'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
		self.assertEqual(actual, expected)

		expected_len = 20
		self.assertEqual (len(data), expected_len)
		
	def test_cleanselog (self):
		log = {'ip': '198.0.200.105', 
				'user_ident': '-', 
				'user_http': '-', 
				'ts': '[14/Jan/2014:09:36:50', 
				'ms': '-0800]', 
				'request': 'GET /svds.com/rockandroll HTTP/1.1', 
				'response_code': '301', 
				'bytes_out': '241', 
				'referrer': '-', 
				'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
		actual = ApacheLog.cleanselog(log)
		expected = {'ip': '198.0.200.105',
				'request_resource': '/svds.com/rockandroll',
				'request_protocol': 'HTTP/1.1',
				'user_ident': '-',
				'user_http': '-',
				'ts': '14/Jan/2014:09:36:50',
				'ms': '-0800',
				'request_method': 'GET',
				'response_code': '301',
				'bytes_out': '241',
				'referrer': '-',
				'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
		self.assertEqual (actual, expected)

	def test_cleaselog_null (self):
		log = {}
		actual = ApacheLog.cleanselog(log)
		expected = {}
		self.assertEqual (actual, expected)

	def test_to_dataframe (self):
		data = utils.dataloader ('data/wslog.dat.template', ApacheLogSchemaRaw, ' ')
		df = utils.to_dataframe (data)
		expected_len = 20
		actual_len = len (df)
		self.assertEqual(actual_len, expected_len) 

if __name__ == '__main__':
	unittest.main()

