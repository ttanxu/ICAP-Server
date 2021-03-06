import socket
import traceback
from StringIO import StringIO

from bufferreader import BufferReader
from icapheader import ICAPHeader

import log
log.openLog('Log/log.txt')

from icapconf import ICAPConf
ICAPConf.parse()
ReqmodHandler = ICAPConf.reqmod()
RespmodHandler = ICAPConf.respmod()
OptionsHandler = ICAPConf.options()

from iohelper import readheader

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost',ICAPConf.port()))
sock.listen(ICAPConf.maxconn())
print 'Open socket at port ' + str(ICAPConf.port()) + ' to listen...'
log.log('Successfully bound socket')
try:
	no = 0
	while True:
		(connSock, addr) = sock.accept()
		print 'Open #' + str(no) + ' socket with address: ' + str(addr)
		log.log('Open #' + str(no) + ' socket with address: ' + str(addr))
		try:
			br = BufferReader(connSock)
			header = readheader(br)

			header = ICAPHeader(header)
			print header.mode
			log.log('Parsed ICAP Header with mode: ' + header.mode)

			if (header.mode == ICAPHeader.Options):
				handler = OptionsHandler(header)
				needreconnect = False

			if (header.mode == ICAPHeader.Reqmod):
				handler = ReqmodHandler(header, br)

			if (header.mode == ICAPHeader.Respmod):
				handler = RespmodHandler(header, br)

			try:
				handler.modify()
				log.log('Modified ' + str(no))
			except BaseException, e:
				traceback.print_exc()
				log.log('Handler Error: ' + str(e))

				strio = StringIO()
				traceback.print_ext(fileobj=strio)
				log.log(strio.getvalue())

			connSock.send(str(handler))
			log.log('Sent ' + header.mode + ' response back to ' + str(addr))
			log.verboselog(str(handler))
		except socket.error, e:
			log.log('Socket Error: ' + str(e))
		except KeyboardInterrupt:
			raise
		except BaseException, e:
			log.log('Error: ' + str(e))
			needreconnect = True
		finally:
			connSock.close()
			log.log('Closing #' + str(no) + ' connSock...')
			print 'Closing #' + str(no) + ' connSock...'
			no += 1
except KeyboardInterrupt:
	pass
except BaseException, e:
	log.log('Error: ' + str(e))
finally:
	sock.close()
	log.log('Successully unbound socket')
	log.closeLog()
	print 'Closing sock and log...'
