from StringIO import StringIO
import gzip
import zlib

linebr = '\r\n'

# To read all line until hitting an empty one
def readheader(reader):
	global linebr

	header = ''
	line = reader.readline()
	while line != '':
		header += (line + linebr)
		line = reader.readline()
	
	return header

# Read chunked payload (Note all ICAP payload use chunked encoding)
def readpayload(reader):
	payload = ''
	numofbytes = int(reader.readline().split()[0], 16)
	while numofbytes > 0:
		payload += reader.readbytes(numofbytes)
		reader.readline() # Empty line expected after each chunk
		numofbytes = int(reader.readline(), 16)

	return payload

# Wrap raw payload into a chunk followed by an 0-length chunk indicating the end of payload
def wrappayload(payload):
	global linebr

	response = (hex(len(payload))[2:] + linebr)
	response += (payload + linebr)

	if len(payload) > 0:
		response += ('0' + linebr + linebr)

	return response

# HTTP GZip compress
def GzipCompress(string):
	strio = StringIO()
	compressor = gzip.GzipFile(fileobj=strio, mode='wb', compresslevel=9)
	compressor.write(string)
	compressor.close()

	return strio.getvalue()

# HTTP GZip Decompress
def GzipDecompress(string):
	return zlib.decompress(string, 16 + zlib.MAX_WBITS)

# HTTP inflation of Deflate
def inflate(string):
	try:
		return zlib.decompress(string, -zlib.MAX_WBITS)
	except zlib.error:
		return zlib.decompress(string)

# HTTP deflation of Deflate
def deflate(string):
	return zlib.compress(string)[2:-4]
