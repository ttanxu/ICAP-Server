from datetime import datetime
import sys

logfile = sys.stdout
linebr = '\n'

verbose = False

def openLog(path):
	global logfile

	logfile = open(path, 'a')

def log(message):
	lines = message.split(linebr)
	for line in lines:
		logfile.write(datetime.now().strftime('%m/%d/%Y %H:%M:%S %Z') + '| ' + line + linebr)

def verboselog(message):
	global verbose

	if not verbose:
		return

	log(message)

def closeLog():
	global logfile

	if logfile != sys.stdout:
		logfile.close()
		logfile = sys.stdout
