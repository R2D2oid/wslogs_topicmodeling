import argparse
import logging
import pickle
from datetime import datetime as dt
import lib.utilities as utils
from model.apachelogschema import ApacheLogSchema, ApacheLogSchemaRaw, ApacheLog 
from model.apachelogmodel import ApacheLogModel

if __name__ == '__main__':
	# python main.py --config config.cfg.template --data data/wslog.dat.template --num_topics 10 --alpha auto --iterations 100 --modelname Agrajag
	parser = argparse.ArgumentParser ()
	parser.add_argument('--config', dest = 'configpath', default = 'config.cfg', help = 'provide config file')
	parser.add_argument('--data', dest = 'datapath', default = 'data/wslog.dat.template', help = 'provide the path to data file in json format')
	parser.add_argument('--num_topics', dest = 'num_topics', type = int, default = '10', help = 'provide number of topics')
	parser.add_argument('--alpha', dest = 'alpha', default = 'auto', help = 'provide alpha parm in lda')
	parser.add_argument('--iterations', dest = 'iterations', type = int, default = 100, help = 'provide the number of iterations to train the model')
	parser.add_argument('--modelname', dest = 'modelname', default = 'output', help = 'provide a path to store the model and experiment tracking info')

	args = parser.parse_args ()
	config = utils.configloader (args.configpath)
	datapath = args.datapath
	num_topics = args.num_topics
	alpha = args.alpha
	iterations = args.iterations
	modelname = args.modelname

	# init logging
	logging.basicConfig (
		filename = config['logging']['logfile'].format (dt.now().date()),
		level = config['logging']['level'],
		format = config['logging']['format'])
	logging.getLogger ().addHandler (logging.StreamHandler())
	logger = logging.getLogger (__name__)

	# load data
	data = utils.dataloader (datapath, ApacheLogSchemaRaw, ' ')
	data = [ApacheLog.format(l) for l in data]
	logger.info ('completed loading data from {}'.format (datapath))
	
	# load feature extraction configs
	featextraction_config = utils.configloader('config.cfg.template')['feat_extraction']

	# init model
	model = ApacheLogModel (data, featextraction_config, num_topics = num_topics, alpha = alpha, iterations = iterations, modelname = modelname)

	# train model
	model.train ()
	logger.info('completed model training')

	# store model, vis, experiment
	pkl = model.pickleit ()
	logger.info ('stored model at {}'.format (pkl))

	vis = model.visulize ()
	logger.info ('stored visulization at {}'.format (vis))

	exp = model.store_experiment ()
	logger.info ('stored experiment parameters at {}'.format (exp))
