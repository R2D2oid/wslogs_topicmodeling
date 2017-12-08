import logging

class ApacheLogSchemaRaw (object):
	ip = 'ip'
	user_ident = 'user_ident'
	user_http = 'user_http'
	ts = 'ts'
	ms = 'ms'
	request = 'request'
	response_code = 'response_code'
	bytes_out = 'bytes_out'
	referrer = 'referrer'
	user_agent = 'user_agent'

	@staticmethod
	def list_members():
		return ['ip', 'user_ident', 'user_http', 'ts', 'ms', 'request', 'response_code', 'bytes_out', 'referrer', 'user_agent']
	
class ApacheLogSchema (object):
	ip = ApacheLogSchemaRaw.ip
	user_ident = ApacheLogSchemaRaw.user_ident
	user_http = ApacheLogSchemaRaw.user_http
	ts = ApacheLogSchemaRaw.ts
	ms = ApacheLogSchemaRaw.ms
	request_method = 'request_method'
	request_resource = 'request_resource'
	request_protocol = 'request_protocol'
	response_code = ApacheLogSchemaRaw.response_code
	bytes_out = ApacheLogSchemaRaw.bytes_out
	referrer = ApacheLogSchemaRaw.referrer
	user_agent = ApacheLogSchemaRaw.user_agent

	@staticmethod
	def list_members():
		return ['ip', 'user_ident', 'user_http', 'ts', 'ms', 'request_method', 'request_resource', 'request_protocol', 'response_code', 'bytes_out', 'referrer', 'user_agent']

class ApacheLog (object):
	@staticmethod
	def format(log):
		''' given a log record in dict format, cleanses unneccessary parts and formats the record '''
		d = {}
		for k in log.keys():
			if k == ApacheLogSchemaRaw.request:
				parts = log[k].split(' ')
				d[ApacheLogSchema.request_method] = parts[0]
				d[ApacheLogSchema.request_resource] = parts[1]
				d[ApacheLogSchema.request_protocol] = parts[2]
			else:
				d[k] = log[k].replace('[', '').replace(']', '')
		return d
