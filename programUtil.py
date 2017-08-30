#!/usr/bin/python
try:
	from subprocess import Popen, PIPE
	from re import split
	from sys import stdout
	import os
	import sys
	import dictFunc
	import systemUtil
except ImportError:
	print "missing modules for programUtil.py"
	sys.exit(1)

#check function status based on binary string	
def functionStatus(functionString, index):
	dict = {'function' : 'functionStatus'}
	stringSize=len(functionString)
	dict['stringSize'] = stringSize
	dict['comment'] = ""
	dict['index'] = index
	if stringSize > index :
		dict['retVal'] = 0
		dict['result'] = functionString[index]
	else:
		dict['retVal'] = 1
		dict['comment'] = "string size is greater than index"
	return dict
	
	
def changeFunctionStatus(functionString, index, value):
	dict = {'function' : 'changeFunctionStatus'}
	stringSize=len(functionString)
	dict['comment'] = ""
	dict['comment'] = dict['comment'] + "\tindex:  " + str(index) + "\n"
	dict['comment'] = dict['comment'] + "\tvalue:  " + str(value) + "\n"
	dict['error'] = ""
	if stringSize > index :
		dict['retVal'] = 0
		s=list(functionString)
		s[index] = str(value)
		dict['comment'] = dict['comment'] + "\ts[index]:  " + str(s[index]) + "\n"
		functionString="".join(s)
		dict['comment'] = dict['comment'] + "\tfunctionString:  " + str(functionString) + "\n"
		dict['result'] = functionString
	else:
		dict['retVal'] = 1
		dict['error'] = "string size is greater than index"
	return dict

def functionStatusWrapReturn ( filePath, key, indexForString, func, *args):
	dict = {'function' : 'functionStatusWrapReturn'}
	dict['comments'] = "functionStatusWrapReturn:  \n\tfilePath:  " +str(filePath)	 + "\n"
	dict['comments'] = dict['comments'] + "\tkey:  " +str(key) + "\n"
	dict['comments'] = dict['comments'] + "\tindexForString:  " +str(indexForString) + "\n"
	retDict2=systemUtil.getValueInfo(str(filePath),key)
	dict['comments'] = dict['comments'] + "getValueInfo comments: \n\tretVal:  " + str(retDict2['retVal']) + "\n"
	dict['getValueInfoTRetVal']=retDict2['retVal'] 
	if retDict2['retVal'] == 0:
		functionString=retDict2['result']
		dict['comments'] = dict['comments'] + "\tfunctionString: " + functionString + "\n"
		retDict=functionStatus(functionString, indexForString)
		dict['comments'] = dict['comments'] + "functionStatus comments:  \n\tretVal: " + str(retDict['retVal']) + "\n"
		dict['comments'] = dict['comments'] + "\tstringSize: " + str(retDict['stringSize']) + "\n"
		dict['comments'] = dict['comments'] + "\tindex: " + str(retDict['index']) + "\n"
		dict['functionStatusRetVal']=retDict['retVal'] 
		if retDict['retVal'] == 0:
			dict['comments'] = dict['comments'] + "\tresult: " + str(retDict['result']) + "\n"
			dict['functionStatusResult']=retDict['result']
			if int(retDict['result']) == 0:
				func ( *args)
				retDict = changeFunctionStatus(functionString, indexForString, 1)
				dict['comments'] = dict['comments'] + "changeFunctionStatus comments: \n" + retDict['comment']
				retDict=systemUtil.updateRaceConditionFile(str(filePath),"functionStatus",retDict['result'])
				dict['comments'] = dict['comments'] + "updateRaceConditionFile comments: \n" + retDict['comment']
	return dict


def functionStatusWrap ( filePath, key, indexForString, func, *args):
	#print  "  filePath:          " +str(filePath)	
	#print  "  key:               " +str(key)	
	#print  "  indexForString:    " +str(indexForString)	
	retDict2=systemUtil.getValueInfo(str(filePath),key)
	#print  "  getValueInfo retVal:    " +str(retDict2['retVal'])	
	if retDict2['retVal'] == 0:
		functionString=retDict2['result']
		#print "    functionString:  " + functionString
		retDict=functionStatus(functionString, indexForString)
		#print "    functionStatus retVal:  " +str(retDict['retVal'])
		#print "    stringSize:  " +str(retDict['stringSize'])
		#print "    index:  " +str(retDict['index'])
		if retDict['retVal'] == 0:
			#print "      result:  " +str(retDict['result'])
			if int(retDict['result']) == 0:
				func ( *args)
				retDict = changeFunctionStatus(functionString, indexForString, 1)
				systemUtil.updateRaceConditionFile(str(filePath),"functionStatus",retDict['result'])
