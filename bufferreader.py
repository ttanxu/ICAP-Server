class BufferReader:
	def __init__(self, socket):
		self._socket = socket
		self._linebr = '\r\n'
		self._block = 4096
		self._buf = ''
		self._bytes = 0
	
	def readline(self):
		lines = self._buf.split(self._linebr, 1)
		while len(lines) < 2:
			block = self._socket.recv(self._block)
			self._buf += block
			self._bytes += len(block)
			lines = self._buf.split(self._linebr, 1)

		line = lines[0]
		self._buf = lines[1]
		return line

	def readbytes(self, length):
		while len(self._buf) < length:
			block = self._socket.recv(self._block)
			self._buf += block
			self._bytes += len(block)

		buf = self._buf[:length]
		self._buf = self._buf[length:]
		return buf

	def bytesofread(self):
		return self._bytes - len(self._buf)

	def setlinebreak(self, linebreak):
		self._linebr = linebreak
