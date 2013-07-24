import sys
sys.path.append('../')
from icaprespmod import RespmodHandler

import json

class MyRespmod(RespmodHandler):
	def __init__(self, header, reader):
		RespmodHandler.__init__(self, header, reader)
	
	def modify(self):
		if 'ctype' in dir(self.respheader) and self.respheader.ctype[:16] == 'application/json':

			root = json.loads(self.respbody)

			words = self.reqheader.uri.split('/')
			if words[2] == 'atv-ext.amazon.com' and self.reqheader.uri.split('/')[5].split('?')[0] == 'GetASINDetails': 
				message = root['message']
				if message['statusCode'] == 'SUCCESS':
					titles = message['body']['titles']
					for title in titles:
						title['synopsis'] = 'Garfield likes it.'

			root['Modifier'] = 'Garfield'

			self.respbody = json.dumps(root, sort_keys=True, indent=4)
