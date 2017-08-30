#!/usr/bin/python
# try:
from programUtil import *
from systemUtil import *

# except ImportError:
# 	print "missing modules for main.py"
# 	sys.exit(1)


def testMain():
	curDir = os.path.dirname(os.path.realpath(__file__))
	sys.path.append(curDir)
	dirName = os.path.dirname(curDir)
	sys.path.append(dirName)
	curDir=os.getcwd()
	filepath=curDir+"/runCheck.txt"
	
	#create race condition file
	retDict=createRaceConditionFile(filepath)
	functionString = "0000"
	updateRaceConditionFile(filepath, "functionStatus", functionString)
	
	#get status of first function
	key="functionStatus"
	retDict2=getValueInfo(filepath,key)
	print  "  getValueInfo retVal:    " +str(retDict2['retVal'])
	if retDict2['retVal'] == 0:
		functionString=retDict2['result']
		print "    functionString:  " + functionString
		retDict=functionStatus(functionString, 0)
		print "  functionStatus retVal:  " +str(retDict['retVal'])
		if retDict['retVal'] == 0:
			print "  result:  " +str(retDict['result'])
			if int(retDict['result']) == 0:
				print "first code"
				retDict = changeFunctionStatus(functionString, 0, 1)
				updateRaceConditionFile(filepath,"functionStatus",retDict['result'])
	
	#get status of third function	
	retDict2=getValueInfo(filepath,key)
	print  "  getValueInfo retVal:    " +str(retDict2['retVal'])
	if retDict2['retVal'] == 0:
		functionString=retDict2['result']
		print "    functionString:  " + functionString
		retDict=functionStatus(functionString, 2)
		print  "  functionStatus retVal:  " +str(retDict['retVal'])
		if retDict['retVal'] == 0:
			print "  result:  " +str(retDict['result'])
			if int(retDict['result']) == 0:
				print "third code"
				retDict = changeFunctionStatus(functionString, 2, 1)
				updateRaceConditionFile(filepath,"functionStatus",retDict['result'])
	
	#get status of fourth function	
	retDict2=getValueInfo(filepath,key)
	print  "  getValueInfo retVal:    " +str(retDict2['retVal'])
	if retDict2['retVal'] == 0:
		functionString=retDict2['result']
		print "    functionString:  " + functionString
		retDict=functionStatus(functionString, 3)
		print  "  functionStatus retVal:  " +str(retDict['retVal'])
		if retDict['retVal'] == 0:
			print "  result:  " +str(retDict['result'])
			if int(retDict['result'])  == 0:
				print "fourth code"
				retDict =changeFunctionStatus(functionString, 3, 1)
				updateRaceConditionFile(filepath,"functionStatus",retDict['result'])
	
	retDict2=getValueInfo(filepath,key)
	functionString=retDict2['result']		
	return functionString

