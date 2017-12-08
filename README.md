# wslogs_topicmodeling
anomaly detection in hosted website logs using topic models

## to run
`python main.py --config config.cfg.template --data data/wslog.dat.template --num_topics 10 --alpha auto --iterations 100 --modelname Agrajag`

## dataset
the template dataset stored at `data/wslog.dat.template` is the head and tail of the raw apache log dataset from https://github.com/silicon-valley-data-science/datasets 
