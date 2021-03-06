from icaphandler import Handler
import sys
sys.path.append('./HttpProtocol')
from httpreqheader import HTTPReqHeader

from iohelper import readheader
from iohelper import readpayload
from iohelper import wrappayload
from iohelper import GzipCompress
from iohelper import GzipDecompress
from iohelper import deflate
from iohelper import inflate

class ReqmodHandler(Handler):
	def __init__(self, header, reader):
		if (header.mode != header.Reqmod):
			raise 'Unsupported', 'ReqmodHandler cannot handle other requests: ' + header.mode

		Handler.__init__(self, header)

		for chunk in header.encapsulated:
			words = chunk.split('=')
			if words[0] == Handler.Reqbody or words[0] == Handler.Nullbody:
				self.reqheader = readheader(reader)

				self.reqheader = HTTPReqHeader(self.reqheader)

			if words[0] == Handler.Reqbody:
				self.reqbody = readpayload(reader)

				# Compressed encoding is generally used in HTTP
				if 'cenc' in dir(self.reqheader):
					print len(self.reqbody)
					print self.reqheader.cenc
					if self.reqheader.cenc == 'gzip':
						self.reqbody = GzipDecompress(self.reqbody)
					if self.reqheader.cenc == 'deflate':
						self.reqbody = inflate(self.reqbody)

	
	def __str__(self):
		if 'encoding' in dir(self.reqheader):
			del self.reqheader.encoding # We don't use chunk for HTTP client

		if 'reqbody' in dir(self):
			if 'cenc' in dir(self.reqheader):
				if self.reqheader.cenc == 'gzip':
					self.reqbody = GzipCompress(self.reqbody)
				if self.reqheader.cenc == 'deflate':
					self.reqbody = deflate(self.body)

			self.reqheader.length = len(self.reqbody)

		self.statuscode = 200 # OK
		self.encapsulated = Handler.Reqheader + '=0'

		response = str(self.reqheader)
		if 'reqbody' in dir(self):
			self.encapsulated += (', ' + Handler.Reqbody + '=' + str(len(response)))
			response += wrappayload(self.reqbody)
		else:
			self.encapsulated += (', ' + Handler.Nullbody + '=' + str(len(response)))

		return Handler.__str__(self) + response
