class ICAPHeader:
	Options = 'OPTIONS'
	Reqmod = 'REQMOD'
	Respmod = 'RESPMOD'

	def __init__(self, header):
		self._linebr = '\r\n'
		
		lines = header.split(self._linebr)
		words = lines[0].split()
		self.mode = words[0]
		self.req = words[1]
		self.uri = '/' + self.req.split('/', 3)[3]
		self.version = words[2]

		self.params = []
		for i in range(1, len(lines)):
			if lines[i] != '':
				words = lines[i].split(': ', 1)
				self.params.append((words[0],words[1]))

		self.allow204 = False
		for (k, v) in self.params:
			if k == 'Host':
				self.host = v
			if k == 'Allow' and '204' in v.split():
				self.allow204 = True
			if k == 'Encapsulated':
				self.encapsulated = v.split(', ')
