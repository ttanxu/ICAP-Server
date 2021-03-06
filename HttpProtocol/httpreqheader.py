class HTTPReqHeader:
	Host = 'Host'
	Accept = 'Accept'
	Length = 'Content-Length'
	Ctype = 'Content-Type'
	Encoding = 'Transfer-Encoding'
	Cenc = 'Content-Encoding'

	def __init__(self, header):
		lines = header.split('\r\n')

		words = lines[0].split()
		self.verb = words[0]
		self.uri = words[1]
		self.version = words[2]

		self.params = []
		self.accept = set()
		for i in range(1, len(lines)):
			if lines[i] != '':
				words = lines[i].split(': ')
				if words[0] == HTTPReqHeader.Host:
					self.host = words[1];
				elif words[0] == HTTPReqHeader.Accept:
					fragments = words[1].split(', ')
					for fragment in fragments:
						subfrags = fragment.split(',')
						for subfrag in subfrags:
							self.accept.add(subfrag.split(';')[0])
				elif words[0] == HTTPReqHeader.Ctype:
					self.ctype = words[1]
				elif words[0] == HTTPReqHeader.Length:
					self.length = int(words[1])
				elif words[0] == HTTPReqHeader.Encoding:
					self.encoding = words[1]
				elif words[0] == HTTPReqHeader.Cenc:
					self.cenc = words[1]
				else:
					self.params.append((words[0], words[1]))

	def __str__(self):
		header = self.verb + ' ' + self.uri + ' ' + self.version + '\r\n'
		if 'host' in dir(self):
			header += (HTTPReqHeader.Host + ': ' + self.host + '\r\n')
		if 'accept' in dir(self):
			line = ''
			for ctype in self.accept:
				line += (ctype + ', ')
			header += (HTTPReqHeader.Accept + ': ' + line[:-2] + '\r\n')
		if 'ctype' in dir(self):
			header += (HTTPReqHeader.Ctype + ': ' + self.ctype + '\r\n')
		if 'length' in dir(self):
			header += (HTTPReqHeader.Length + ': ' + str(self.length) + '\r\n')
		if 'encoding' in dir(self):
			header += (HTTPReqHeader.Encoding + ': ' + self.encoding + '\r\n')
		if 'cenc' in dir(self):
			header += (HTTPReqHeader.Cenc + ': ' + self.cenc + '\r\n')

		for (k, v) in self.params:
			header += (str(k) + ': ' + str(v) + '\r\n')
		header += '\r\n'

		return header
