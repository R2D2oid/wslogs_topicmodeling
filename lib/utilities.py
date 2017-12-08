import configparser
from csv import reader
import pandas as pd

def flatten_nested_dct (dct):
	''' flattens a nested dictionary. for example, a nested json which goes deeper than one layer '''
	result = {}
	if type(dct) == dict:
		for k in dct.keys():
			val = dct[k]
			if type (val) == dict:
				content = flatten_nested_dct (val)
				for k_sub in content:
					k_aug = '{}_{}'.format(k, k_sub)
					result[k_aug] = content[k_sub]
			else:
				result[k] = val
	return result

def configloader (configpath):
	''' loads the config file from the provided path'''
	cp = configparser.RawConfigParser()
	cp.read(configpath)
	config = {}

	section = {}
	tag = 'samplesection'
	section['var'] = cp.get(tag, 'var')
	config[tag] = section

	section = {}
	tag = 'logging'
	section['logfile'] = cp.get(tag, 'logfile')
	section['format'] = cp.get(tag, 'format')
	section['level'] = cp.getint(tag, 'level')
	config[tag] = section

	section = {}
	tag = 'feat_extraction'
	section['relevant_fields'] = list (cp.get (tag, 'relevant_fields').split (','))
	section['tokenize_fields'] = list (cp.get (tag, 'tokenize_fields').split (','))
	section['sizify_fields'] = list (cp.get (tag, 'sizify_fields').split (','))
	section['rangify_fields'] = list (cp.get (tag, 'rangify_fields').split (','))
	section['wordify_fields'] = list (cp.get (tag, 'wordify_fields').split (','))
	section['entropy_fields'] = list (cp.get (tag, 'entropy_fields').split (','))
	section['invalid_words'] = list (cp.get (tag, 'invalid_words').split (','))
	config[tag] = section

	return config

def dataloader (datapath, schema, delim = ' '):
	''' given path of a datafile and its schema, as a list, this function loads the data into a list of dicts '''
	data = []
	with open (datapath, 'r') as f:
		for values in reader(f, delimiter = delim):
			d = {}
			if len (values) != len (schema.list_members()):
				print ('format of content does not match the schema')
				continue
			for (k,v) in zip(schema.list_members(), values):
				d[k] = v
			data.append(d)
 	return data

def to_dataframe (data):
	df = pd.DataFrame (data)
	df = df.convert_objects (convert_numeric = True)
	return df
