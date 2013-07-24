from datetime import datetime

class Handler:
	Reqheader = 'req-hdr'
	Reqbody = 'req-body'
	Nullbody = 'null-body'
	Respheader = 'res-hdr'
	Respbody = 'res-body'

	statuscode = {
			100 : 'Continue after ICAP Preview',
			200 : 'OK',
			204 : 'No modifications needed',
			400 : 'Bad request',
			404 : 'ICAP Service not found',
			405 : 'Method not allowed for service',
			408 : 'Request timeout',
			418 : 'Bad composition',
			500 : 'Server error',
			501 : 'Method not implemented',
			502 : 'Bad Gateway',
			503 : 'Service overloaded',
			505 : 'ICAP version not supported by server'
	}

	def __init__(self, header):
		self.params = []
		self.icapheader = header

	def modify(self):
		return


	def __str__(self):
		if 'version' not in dir(self):
			self.version = 'ICAP/1.0'
		response = self.version + ' ' + str(self.statuscode) + ' ' + Handler.statuscode[self.statuscode] + '\r\n'

		response += ('Date: ' + datetime.utcnow().strftime('%a, %d %b %Y  %H:%M:%S GMT') + '\r\n')
		response += ('Connection: close\r\n')
		response += ('Encapsulated: ' + self.encapsulated + '\r\n')
		
		if 'istag' not in dir(self):
			self.istag = 'Garfield'
		response += ('ISTag: ' + self.istag + '\r\n')
		
		for (k, v) in self.params:
			if k != 'Date' and k != 'Connection' and k != 'ISTag':
				response += (str(k) + ': ' + str(v) + '\r\n')

		response += '\r\n'
		
		return response
