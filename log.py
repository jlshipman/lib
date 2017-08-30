#!/usr/bin/python
import sys
import os
import logging
from datetime import *

sys.path.append('lib')
import directory
		
class log:
	logFileName = ""
	
	def __init__(self, outputPrint=True):
		self.outputPrint = outputPrint
		
		
	def setData(self, prefix, loggerName):
		self.prefix = prefix
		now = datetime.now()
		newfilename= "LOG/log_" + now.strftime("%Y_%m_%d_%H_%M")
		self.logFileName = newfilename
		logging.basicConfig(filename=newfilename, format='%(asctime)s %(message)s', datefmt='%Y_%m_%d %H:%M:%S')	
		log = logging.getLogger(loggerName)

	def setData2(self, prefix, loggerName, dirPath):
		self.prefix = prefix
		now = datetime.now()
		newfilename= dirPath + "/log_" + now.strftime("%Y_%m_%d_%H_%M")
		self.logFileName = newfilename
		logging.basicConfig(filename=newfilename, format='%(asctime)s %(message)s', datefmt='%Y_%m_%d %H:%M:%S')	
		log = logging.getLogger(loggerName)
	
	def setPrefix(self, prefix):
		self.prefix = prefix
		
	def setOutputPrint (self, outputPrint):
		self.outputPrint = outputPrint
	
	def logfileAsString (self):
		f = open (self.logFileName, "r")
		resultString = f.read()
		f.close ()	
		return resultString
		
	def logName (self):
		return self.logFileName
		
	def output(self,type,input):
		if self.outputPrint == True:
			now = datetime.now()
			print ( now.strftime('%Y_%m_%d %H:%M:%S') + " "+ self.prefix + " "+ type + input)
	
	def debug (self, input):
		logging.warning( "debug: " + input)
		self.output("debug: ",input)
	
	def info (self, input):
		logging.warning("info:  " + input)
		self.output("info: ",input)

	def infoMessage (self, input, message):
		logging.warning("info:  " + input)
		self.output("info: ",input)
		message = message + input + "\n"
		return message
		
	def warn (self, input):
		logging.warning("WARN:  " + input)
		self.output("WARN: ",input)
		
	def warnMessage (self, input, message):
		logging.warning("WARN:  " + input)
		self.output("WARN: ",input)
		message = message + input + "\n"
		return message
		
	def abortExit (self, input):
		logging.warning("ABORT:  " + input)
		self.output("ABORT: ",input)
		sys.exit(1)
	
	def abort (self, input):
		logging.warning("ABORT:  " + input)
		self.output("ABORT: ",input)
		
	def logDelete(self, dir, count, save):
		count = int (count)
		save = int (save)
		numToDelete=count-save+1
		if count > save:
			numToDelete=count-save+1
			files=directory.listFiles(dir, "log_")
			for x in range(0, numToDelete):
				os.unlink(files[x])
		
		
	
