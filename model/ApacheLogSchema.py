import logging

class ApacheLogSchemaRaw:
	f0_ip = 'f0_ip'
	f1_user_ident = 'f1_user_ident'
	f2_user_http = 'f2_user_http'
	f3_ts = 'f3_ts'
	f4_ms = 'f4_ms'
	f5_request = 'f5_request'
	f6_response_code = 'f6_response_code'
	f7_bytes_out = 'f7_bytes_out'
	f8_referrer = 'f8_referrer'
	f9_user_agent = 'f9_user_agent'

	@staticmethod
	def list_members():
		return sorted([attr for attr in dir(ApacheLogSchemaRaw) if not callable(getattr(ApacheLogSchemaRaw, attr)) and not attr.startswith('__')])
	
class ApacheLogSchema:
	f0_ip = ApacheLogSchemaRaw.f0_ip
	f1_user_ident = ApacheLogSchemaRaw.f1_user_ident
	f2_user_http = ApacheLogSchemaRaw.f2_user_http
	f3_ts = ApacheLogSchemaRaw.f3_ts
	f4_ms = ApacheLogSchemaRaw.f4_ms
	f5_request_method = 'f5_request_method'
	f6_response_code = ApacheLogSchemaRaw.f6_response_code
	f7_bytes_out = ApacheLogSchemaRaw.f7_bytes_out
	f8_referrer = ApacheLogSchemaRaw.f8_referrer
	f9_user_agent = ApacheLogSchemaRaw.f9_user_agent
	f10_request_resource = 'f10_request_resource'
	f11_request_protocol = 'f11_request_protocol'

	@staticmethod
	def list_members():
		return sorted([attr for attr in dir(ApacheLogSchema) if not callable(getattr(ApacheLogSchema, attr)) and not attr.startswith('__')])

class ApacheLog:
	@staticmethod
	def cleanselog(log):
		''' given a log record in dict format, cleanses unneccessary parts and formats the record '''
		d = {}
		for k in log.keys():
			if k == ApacheLogSchemaRaw.f5_request:
				parts = log[k].split(' ')
				d[ApacheLogSchema.f5_request_method] = parts[0]
				d[ApacheLogSchema.f10_request_resource] = parts[1]
				d[ApacheLogSchema.f11_request_protocol] = parts[2]
			else:
				d[k] = log[k].replace('[', '').replace(']', '')
		return d
