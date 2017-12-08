import sys
sys.path.append ('.')
import unittest
import string
import lib.utilities as utils
from model.apachelogmodel import ApacheLogModel
from model.apachelogschema import ApacheLogSchemaRaw, ApacheLog

class TestUtilities (unittest.TestCase):
	def test_entropy (self):
		actual = ApacheLogModel.entropy ('dontpanic')
		actual = round (actual, 2)
		expected = 2.95
		self.assertEqual (actual, expected)

	def test_derive_ranges (self):
		data = utils.dataloader ('data/wslog.dat.template', ApacheLogSchemaRaw, ' ')
		data = [ApacheLog.format(l) for l in data]
		featext_config = utils.configloader('config.cfg.template')['feat_extraction']
		model = ApacheLogModel (data, featext_config)
		actual = model.derive_stats ()
		expected = {'bytes_out_val': {'high': 14308.57885358002, 'med': 5101, 'low': 3518}, 
				'referrer_len': {'high': 52.121734779245941, 'med': 30, 'low': 28}, 
				'request_resource_len': {'high': 64.657561374216158, 'med': 43, 'low': 37}, 
				'request_resource_ent': {'high': 4.4115352724758283, 'med': 4, 'low': 3}, 
				'user_agent_ent': {'high': 5.0920380749115814, 'med': 5, 'low': 5}, 
				'referrer_ent': {'high': 6.4544661178668585, 'med': 3, 'low': 3}}
		self.assertEqual (actual, expected)

	def test_extract_bows (self):
		data = utils.dataloader ('data/wslog.dat.template', ApacheLogSchemaRaw, ' ')
		data = [ApacheLog.format(l) for l in data]
		featext_config = utils.configloader('config.cfg.template')['feat_extraction']
		model = ApacheLogModel (data, featext_config)
		actual = model.extract_bows (data)[0]
		expected = ['_bytes_out_val_low', '_referrer_ent_low', '_user_agent_ent_veryhigh', '_request_resource_ent_med', 
				'_referrer_len_low', '_request_resource_len_low', '_301', 'mozilla', 'macintosh', 'intel mac os x', 
				'applewebkit', 'khtml', 'like gecko', 'chrome', '... safari', 'svds.com', 'rockandroll']
		self.assertEqual (actual, expected)

	def test_is_number (self):
		s = '42.01'
		actual = ApacheLogModel.is_number(s)
		expected = True
		self.assertEqual (actual, expected)

		s = '42,01'
		actual = ApacheLogModel.is_number(s)
		expected = True
		self.assertEqual (actual, expected)

		s = 'thanksforallthefish'
		actual = ApacheLogModel.is_number(s)
		expected = False
		self.assertEqual (actual, expected)
		
	def test_csplit (self):
		s = 'a,b-c|d_e*f'
		delims = string.punctuation
		actual = ApacheLogModel.csplit (s, delims)
		expected = ['a', 'b', 'c', 'd', 'e', 'f']
		self.assertEqual (actual, expected)
	
	def test_train (self):
		data = utils.dataloader ('data/wslog.dat.template', ApacheLogSchemaRaw, ' ')
		data = [ApacheLog.format(l) for l in data]
		featext_config = utils.configloader('config.cfg.template')['feat_extraction']
		model = ApacheLogModel (data, featext_config)
		tm = model.train()
		print (tm)
		print(tm.show_topics())



if __name__ == '__main__':
	unittest.main()

