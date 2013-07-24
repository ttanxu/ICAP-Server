from datetime import datetime

class HTTPRespHeader:
	Length = 'Content-Length'
	Ctype = 'Content-Type'
	Date = 'Date'
	Encoding = 'Transfer-Encoding'
	Cenc = 'Content-Encoding'
	
	statuscode = {
			100 : 'Continue',
			101 : 'Switching Protocols',
			200 : 'OK',
			201 : 'Created',
			202 : 'Accepted',
			203 : 'Non-Authoritative Information',
			204 : 'No Content',
			205 : 'Reset Content',
			206 : 'Partial Content',
			300 : 'Multiple Choices',
			301 : 'Moved Permanently',
			302 : 'Found',
			303 : 'See Other',
			304 : 'Not Modified',
			305 : 'Use Proxy',
			306 : '(Unused)',
			307 : 'Temporary Redirect',
			400 : 'Bad Request',
			401 : 'Unauthorized',
			402 : 'Payment Required',
			403 : 'Forbidden',
			404 : 'Not Found',
			405 : 'Method Not Allowed',
			406 : 'Not Acceptable',
			407 : 'Proxy Authentication Required',
			408 : 'Request Timeout',
			409 : 'Conflict',
			410 : 'Gone',
			411 : 'Length Required',
			412 : 'Precondition Failed',
			413 : 'Request Entity Too Large',
			414 : 'Request-URI Too Long',
			415 : 'Unsupported Media Type',
			416 : 'Requested Range Not Satisfiable',
			417 : 'Expectation Failed',
			500 : 'Internal Server Error',
			501 : 'Not Implemented',
			502 : 'Bad Gateway',
			503 : 'Service Unavailable',
			504 : 'Gateway Timeout',
			505 : 'HTTP Version Not Supported'
		}

	def __init__(self, header):
		lines = header.split('\r\n')
		words = lines[0].split()

		self.version = words[0]
		self.statuscode = int(words[1])

		self.params = []
		for i in range(1, len(lines)):
			if lines[i] != '':
				words = lines[i].split(': ')
				if words[0] == HTTPRespHeader.Length:
					self.length = int(words[1])
				elif words[0] == HTTPRespHeader.Ctype:
					self.ctype = words[1]
				elif words[0] == HTTPRespHeader.Date:
					self.date = words[1]
				elif words[0] == HTTPRespHeader.Encoding:
					self.encoding = words[1]
				elif words[0] == HTTPRespHeader.Cenc:
					self.cenc = words[1]
				else:
					self.params.append((words[0], words[1]))

	def __str__(self):
		response = self.version + ' ' + str(self.statuscode) + ' ' + HTTPRespHeader.statuscode[self.statuscode] + '\r\n'

		if 'date' in dir(self):
			response += (HTTPRespHeader.Date + ': ' + self.date + '\r\n')
		else:
			response += (HTTPRespHeader.Date + ': ' + datetime.utcnow().strftime('%a, %d %b %Y  %H:%M:%S GMT'))
		if 'ctype' in dir(self):
			response += (HTTPRespHeader.Ctype + ': ' + self.ctype + '\r\n')
		
		if 'cenc' in dir(self):
			response += (HTTPRespHeader.Cenc + ': ' + self.cenc + '\r\n')

		if 'length' in dir(self):
			response += (HTTPRespHeader.Length + ': ' + str(self.length) + '\r\n')

		for (k, v) in self.params:
			response += (str(k) + ': ' + str(v) + '\r\n')

		response += '\r\n'

		return response
