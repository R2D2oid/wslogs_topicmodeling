import logging
import string
import math
import numpy
import urllib
import pickle
import gensim
import pyLDAvis.gensim
from datetime import datetime as dt
import lib.utilities as utils
from lib.enums import Ops, Levels

class ApacheLogModel (object):
	def __init__(self, data, featextraction_configs, num_topics = 10, alpha = 'auto', iterations = 100, modelname = 'amodel'):
		# model training configs
		self.data = data
		self.num_topics = num_topics
		self.alpha = alpha
		self.iterations = iterations
		self.modelname = modelname

		# feature extraction configs
		configs = featextraction_configs
		self.relevant_fields = configs['relevant_fields']
		self.wordify_fields = configs['wordify_fields']
		self.rangify_fields =  configs['rangify_fields']
		self.sizify_fields = configs['sizify_fields']
		self.tokenize_fields = configs['tokenize_fields']
		self.entropy_fields = configs['entropy_fields']
		self.invalid_words = configs['invalid_words']
		self.delimiters = string.punctuation.replace ('.','/')

	def derive_stats (self, data = None):
		data = self.data if data == None else data
		df = utils.to_dataframe (self.data)
		ops = {}
		ops[Ops._val] = list (set (df.columns).intersection(self.rangify_fields))
		ops[Ops._ent] = list (set (df.columns).intersection(self.entropy_fields))
		ops[Ops._len] = list (set (df.columns).intersection(self.sizify_fields)) 
		
		d = {}
		for k in ops.keys():
			cols = ops[k]
			for col in cols:
				if k == Ops._len:
					stats = df[col].str.len ().describe ()
				elif k == Ops._ent:
					stats = df[col].apply (lambda s: self.entropy (str (s)) ).describe ()
				else:
					stats = df[col].describe ()
				ths = {}
				# assumes gaussian distribution
				ths[Levels._low] = int (stats ['25%'])
				ths[Levels._med] = int (stats ['50%']) 
				ths[Levels._high]= int (stats ['75%']) + 2 * stats ['std']
				d['{}_{}'.format (col, k)] = ths
		return d
		
	@staticmethod
	def entropy (s):
		iterator = (ord(c) for c in string.printable)
		entropy = 0
		for c in iterator:
			p_c = float (s.count (chr(c))) / len (s)
			if p_c > 0:
				entropy = entropy - (p_c * math.log (p_c, 2))
		return entropy
		
	def extract_words (self, log, params):
		words = []
		relevant_fields = set (log.keys())
		r_fields = relevant_fields.intersection (self.rangify_fields)
		for f in r_fields:
			words.append (self.rangify (log, f, params, op = Ops._val))

		e_fields = relevant_fields.intersection (self.entropy_fields)
		for f in e_fields:
			words.append (self.rangify (log, f, params, op = Ops._ent))

		s_fields = relevant_fields.intersection (self.sizify_fields)
		for f in s_fields:
			words.append (self.rangify (log, f, params, op = Ops._len))
	
		w_fields = relevant_fields.intersection (self.wordify_fields)
		for f in w_fields:
			words.append (self.wordify (log[f]))

		t_fields = relevant_fields.intersection (self.tokenize_fields)
		for f in t_fields:
			clean_txt = urllib.unquote (log[f]).lower ()
			clean_txt = self.strip_numbers (clean_txt)
			tokens = self.csplit (clean_txt, self.delimiters)
			words.extend (tokens) 
			
		words = [w for w in words if (w not in self.invalid_words and w not in string.printable and not self.is_number(w))]
		return words
		
	
	@staticmethod
	def strip_numbers (s):
		return ''.join ([i for i in s if not i.isdigit()])
	
	@staticmethod
	def is_number (s):
		try: 
			return isinstance(float (s.replace (',','')), float)
		except ValueError as e:	
			return False
		
	@staticmethod 
	def csplit (s, delims):
		d = delims[0]
		for delim in delims[1:]:
			s = s.replace(delim, d)
		
		return [i.strip() for i in s.split(d)]

	def wordify (iself, s):
		word = '_{}'.format(str(s).upper())
		return word

	def rangify (self, log, field, params, op):
		ths = params ['{}_{}'.format(field, op)]
		if op == Ops._len:
			value = int (len (log[field]))
		elif op == Ops._ent:
			value = self.entropy (log[field])
		else:
			try:	value = int (log[field])
			except ValueError:
				value = -1

		if value > ths[Levels._high]:
			return '_{}_{}_{}'.format (field, op, Levels._veryhigh)
		elif value > ths[Levels._med]:
			return '_{}_{}_{}'.format (field, op, Levels._high)
		elif value > ths[Levels._low]:
			return '_{}_{}_{}'.format (field, op, Levels._med)
		else:
			return '_{}_{}_{}'.format (field, op, Levels._low)

	def get_data_params (self, data = None):
		data = self.data if data == None else data
		params = self.derive_stats ()
		return params

	def train (self):
		docs = self.extract_bows (self.data)
		dictionary = gensim.corpora.Dictionary (docs)
		bows = [dictionary.doc2bow (d) for d in docs]
		self.docs = docs
		self.bows = bows
		self.dictionary = dictionary
		lda = gensim.models.ldamodel.LdaModel
		self.model = lda (bows, num_topics = self.num_topics, id2word = dictionary, alpha = self.alpha, passes = self.iterations)
		self.model.show_topics ()
		return self.model

	def extract_bows (self, data = None):
		docs = []
		data = self.data if data == None else data
		params = self.get_data_params (data)
		for l in data:
			doc = self.extract_words(l, params)
			docs.append (doc)
		return docs

	def visulize (self):
		fname = 'output/vis_{}_{}.html'.format(self.modelname, dt.now().date())
		vis = pyLDAvis.gensim.prepare (self.model, self.bows, self.dictionary)
		pyLDAvis.save_html (vis, fname)	
		return fname

	def pickleit (self):
		fname = 'output/model_{}_{}.pkl'.format(self.modelname, dt.now().date())
		pickle.dump (self.model, open (fname, 'w'))
		return fname

	def store_experiment (self):
		fname = 'output/exp_{}_{}.pkl'.format(self.modelname, dt.now().date())
		exp = []
		exp.extend ([('model name', self.modelname), 
				('num topics', self.num_topics), 
				('iterations', self.iterations), 
				('dataset size', len(self.data)), 
				('alpha', self.alpha), 
				('wordify fields', self.wordify_fields), 
				('rangify fields', self.rangify_fields), 
				('sizify fields', self.sizify_fields),
				('tokenize fields', self.tokenize_fields),
				('entropy fields', self.entropy_fields),
				('invalid words', self.invalid_words)])
		with open (fname, 'w') as f:
			for tup in exp:	
				f.write ('{} : {}\n'.format (tup[0], tup[1]))	
