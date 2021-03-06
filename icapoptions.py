from icaphandler import Handler
from icapheader import ICAPHeader

from icapconf import ICAPConf

class OptionsHandler(Handler):
	def __init__(self, header):
		Handler.__init__(self, header)

		if header.mode != ICAPHeader.Options:
			raise 'Unsupported', 'OptionsHandler cannot handle other requests: ' + header.mode

		self.statuscode = 200; # OK

		words = header.uri.split('/')
		method = words[len(words) - 1].split('?')[0]
		if method == 'request':
			self.methods = 'REQMODE'
		if method == 'response':
			self.methods = 'RESPMODE'

		self.service = 'Simple ICAP Server by Garfield'
		self.encapsulated = 'null-body=0' # No additional body/payload for Options response
		self.maxconnection = ICAPConf.maxconn()
	
	def __str__(self):
		self.params.append(('Methods', self.methods))
		self.params.append(('Service', self.service))
		self.params.append(('Max-Connection', self.maxconnection))

		return Handler.__str__(self)
