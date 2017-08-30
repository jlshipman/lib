#!/usr/bin/python
try:
	from subprocess import Popen, PIPE
	from re import split
	from sys import stdout
	import os
	import sys
	import fileFunctions
	import dictFunc
except ImportError:
	print "missing modules for systemUtil.py"
	sys.exit(1)

class Proc(object):
    ''' Data structure for a processes . The class properties are
    process attributes '''
    def __init__(self, procInfo):
        self.user = procInfo[0]
        self.pid = procInfo[1]
        self.cpu = procInfo[2]
        self.mem = procInfo[3]
        self.vsz = procInfo[4]
        self.rss = procInfo[5]
        self.tty = procInfo[6]
        self.stat = procInfo[7]
        self.start = procInfo[8]
        self.time = procInfo[9]
        self.cmd = procInfo[10]

    def to_str(self):
        ''' Returns a string containing minimalistic info
        about the process : user, pid, and command '''
        return '%s %s %s' % (self.user, self.pid, self.cmd)

def getProcList():
    ''' Retrieves a list [] of Proc objects representing the active
    process list list '''
    procList = []
    subProc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    #Discard the first line (ps aux header)
    subProc.stdout.readline()
    for line in subProc.stdout:
        #The separator for splitting is 'variable number of spaces'
        procInfo = split(" *", line.strip())
        procList.append(Proc(procInfo))
    return procList
		
def getPID():
	dict = {'function' : 'getPID'}
	pid = os.getpid()
	stringPid = str(pid)	
	ppid = os.getppid()
	
	stringPpid = str(ppid)
	dict['pid'] = stringPid
	dict['ppid'] = stringPpid
	dict['retVal'] = stringPid
	return dict

#create a file to be checked to avoid race conditions	
def createRaceConditionFile(filePath):
	dict = {'function' : 'createRaceConditionFile'}
	retDict = {}
	if fileFunctions.fileExist ( filePath ):
		#read file into dictionary
		dict['fileExistPrior'] = "yes"
		#access pid from file
		sep=","
		retDict=dictFunc.fileToDict( filePath, sep )
		filePid=int(retDict['pid'])
		
		#get pid for process
		retDict2=getPID()
		processPidString = retDict2['pid']
		processPid=int(processPidString)
		dict['pid']=processPidString
		
		#if pid from file is the same as the processes pid
		if processPid == filePid:
			#then return a 1
			dict['retVal'] = 1
			dict['comment'] = "process is still running"
		else:
			#get pre-existing info except for pid
			retDict=dictFunc.fileToDict( filePath, sep )	
			
			#remove file and return a 0
			dict['retVal'] = 0			
			os.unlink(filePath)
			fileFunctions.fileCreate( filePath )
			
			stringToWrite="pid,"+processPidString+"\n"
			for key in retDict:
				if key != "pid":
					stringToWrite=stringToWrite + key + "," + retDict[key] + "\n"
			fileFunctions.writeToFile(stringToWrite, filePath)
			dict['comment'] = "race condition file exists, but process is stopped"
	else:
		dict['retVal'] = 0
		dict['fileExistPrior'] = "no"
		#get pid for process
		retDict2=getPID()
		processPidString = retDict2['pid']
		processPid=int(processPidString)
		dict['pid']=processPidString
		
		fileFunctions.fileCreate( filePath )
		#create a dictionary and write contents to file
		stringToWrite="pid,"+processPidString+"\n"
		stringToWrite=stringToWrite+"functionStatus,0"
		fileFunctions.writeToFile(stringToWrite, filePath)
		dict['comment'] = "race condition file does not exists"
		
	return dict
	
def getValueInfo	(filePath,key):
	dict = {'function' : 'getKeyValueInfo'}
	retDict = {}
	if fileFunctions.fileExist ( filePath ):
		sep=","
		retDict=dictFunc.fileToDict( filePath, sep )
		value = retDict.get(key)
		if value != None:
			retDict[key]=value
			dict['retVal'] = 0
			dict['result'] = value
		else:
			dict['retVal'] = 1
			dict['comment'] = "key does not exist in dictionary"
	else:
		#there is no race condition file
		dict['retVal'] = 1
		dict['comment'] = "there is no race condition file"
		
	return dict
def updateRaceConditionFile(filePath,key,value):
	dict = {'function' : 'updateRaceConditionFile'}
	retDict = {}
	dict['retVal'] = 0
	dict['comment'] = ""
	dict['comment'] = dict['comment'] +  "\tfilePath: " + filePath + "\n"
	dict['comment'] = dict['comment'] +  "\tkey: " + key + "\n"
	dict['comment'] = dict['comment'] +  "\tvalue: " + value + "\n"
	dict['filePath'] = filePath
	if fileFunctions.fileExist ( filePath ):
		#access pid from file
		sep=","
		retDict=dictFunc.fileToDict( filePath, sep )
		retDict[key]=value
		dict['comment'] = dict['comment'] + "\tnew value:  "  + str(value) + " for  key:  " + key + "\n"
		os.unlink(filePath)
		dictFunc.dictToFile(retDict, filePath, sep)
		dict[key]=value
	else:
		#there is no race condition file
		dict['retVal'] = 1
		dict['comment'] = "there is no race condition file"
	return dict