#!/usr/bin/python

class funcReturn:        
    #Common base class for functions'
	def __init__(self, name, retVal = 1, found = 1):
		self.name  = name
		self.comment  = ""
		self.stdout  = ""
		self.stderr  = ""
		self.result  = ""
		self.retVal  = retVal
		self.found  = found
		self.remed = ""
		self.stage = ""
		self.error = ""
		self.command = ""
		
	def getName (self):
		return self.name
	def setName (self, value):
		self.name = value
				
	def getComment (self):
		return self.comment
	def setComment (self, value):
		self.comment = value
	
	def getStdout (self):
		return self.stdout
	def setStdout (self, value):
		self.stdout = value

	def getStderr (self):
		return self.stderr
	def setStderr (self, value):
		self.stderr = value

	def getResult (self):
		return self.result
	def setResult (self, value):
		self.result = value

	def getRetVal (self):
		return self.retVal
	def setRetVal (self, value):
		self.retVal = value

	def getFound (self):
		return self.found
	def setFound (self, value):
		self.found = value

	def getRemed (self):
		return self.remed
	def setRemed (self, value):
		self.remed = value
		
	def getStage (self):
		return self.stage
	def setStage (self, value):
		self.stage = value

	def getError (self):
		return self.error
	def setError (self, value):
		self.error = value
		
	def getCommand (self):
		return self.command
	def setCommand (self, value):
		self.command = value
