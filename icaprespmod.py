from icaphandler import Handler
import sys
sys.path.append('./HTTPProtocol')
from httprespheader import HTTPRespHeader
from httpreqheader import HTTPReqHeader

from iohelper import readheader
from iohelper import readpayload
from iohelper import wrappayload
from iohelper import GzipCompress
from iohelper import GzipDecompress
from iohelper import deflate
from iohelper import inflate

class RespmodHandler(Handler):
	def __init__(self, header, reader):
		if header.mode != header.Respmod:
			raise 'Unsupported', 'RespmodHandler cannot handle other requests: ' + header.mode

		Handler.__init__(self, header)

		for chunk in header.encapsulated:
			words = chunk.split('=')
			if words[0] == Handler.Reqheader:
				header = readheader(reader)

				self.reqheader = HTTPReqHeader(header)

			if words[0] == Handler.Respheader:
				header = readheader(reader)

				self.respheader = HTTPRespHeader(header)

			if words[0] == Handler.Respbody:
				self.respbody = readpayload(reader)

				# Compressed encoding is generally implemented in HTTP
				if 'cenc' in dir(self.respheader):
					if self.respheader.cenc == 'gzip':
						self.respbody = GzipDecompress(self.respbody)
					if self.respheader.cenc == 'deflate':
						self.respbody = inflate(self.respbody)

	def __str__(self):
		if 'encoding' in dir(self.respheader):
			del self.respheader.encoding # We don't use chunk for HTTP client

		if 'respbody' in dir(self):
			if 'cenc' in dir(self.respheader):
				if self.respheader.cenc == 'gzip':
					self.respbody = GzipCompress(self.respbody)
				if self.respheader.cenc == 'deflate':
					self.respbody = deflate(self.respbody)

			self.respheader.length = len(self.respbody)
		
		self.statuscode = 200 # OK
		self.encapsulated = Handler.Respheader + '=0'

		response = str(self.respheader)
		if 'respbody' in dir(self):
			self.encapsulated += (', ' + Handler.Respbody + '=' + str(len(response)))
			response += wrappayload(self.respbody)
		else:
			self.encapsulated += (', ' + Handler.Nullbody + '=' + str(len(response)))

		return Handler.__str__(self) + response
