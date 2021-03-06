import os
import sys

import log

# Configuration class for Simple ICAP Server
class ICAPConf:
	__port = 9064 # Default port
	__maxconn = 1024 # Default Max Connections
	__conf = 'Conf/icap.conf' # Configuration file
	__verbose = False # If true to output verbose log

	__reqmod = 'icapreqmod.py$ReqmodHandler'
	__respmod = 'icaprespmod.py$RespmodHandler'
	__options = 'icapoptions.py$OptionsHandler'

	@staticmethod
	def parse():
		with open(ICAPConf.__conf) as f:
			for line in f:
				stripped = line.lstrip().rstrip()
				if stripped == '' or stripped[0] == '#':
					continue

				words = stripped.split()
				if words[0] == 'icap_port':
					ICAPConf.__port = int(words[1])
					log.log('Set port = ' + words[1])

				elif words[0] == 'max_conn':
					ICAPConf.__maxconn = int(words[1])
					log.log('Set max_conn = ' + words[1])
				
				elif words[0] == 'reqmod':
					ICAPConf.__reqmod = words[1]
					log.log('Set ReqmodHandler = ' + words[1])

				elif words[0] == 'respmod':
					ICAPConf.__respmod = words[1]
					log.log('Set RespmodHandler = ' + words[1])

				elif words[0] == 'verbose':
					ICAPConf.__verbose = bool(words[1])
				else:
					log.log('Cannot parse configuration: ' + stripped + ' Ignored!')


		ICAPConf.__reqmod = ICAPConf.__load(ICAPConf.__reqmod)
		ICAPConf.__respmod = ICAPConf.__load(ICAPConf.__respmod)
		ICAPConf.__options = ICAPConf.__load(ICAPConf.__options)

	@staticmethod
	def __load(path):
		words = path.split('$')
		module = words[0]
		dirname = os.path.dirname(os.path.abspath(module))
		filename, ext = os.path.splitext(os.path.basename(module))

		if dirname:
			sys.path.insert(0, dirname)
		module = __import__(filename)
		if dirname:
			del sys.path[0]

		clazz = words[1]
		clazz = getattr(module, clazz)

		return clazz

	@staticmethod
	def port():
		return ICAPConf.__port

	@staticmethod
	def maxconn():
		return ICAPConf.__maxconn

	@staticmethod
	def reqmod():
		return ICAPConf.__reqmod

	@staticmethod
	def respmod():
		return ICAPConf.__respmod

	@staticmethod
	def options():
		return ICAPConf.__options

	@staticmethod
	def verbose():
		return ICAPConf.__verbose
