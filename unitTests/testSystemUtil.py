#!/usr/bin/python	
import unittest
import os, sys
import subprocess
import re

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
outPutFile = curDir+"/output.txt"
raceConditionOutPutFile = curDir+"/raceConditionOutPutFile.txt"
raceConditionOutPutFile2= curDir+"/raceConditionOutPutFile2.txt"
raceConditionOutPutFile3= curDir+"/raceConditionOutPutFile3.txt"
import systemUtil
import comWrap
import fileFunctions
import dictFunc

class TestSystemUtil(unittest.TestCase):
 	print "Tests for `systemUtil.py`."
 	
	def setUp(self):
		pass
 
	def testGetPID(self):
		#test requires hombrew installed and pstree installed from hombrew
		print "  testGetPID"
		retDict=systemUtil.getPID()
		pid=retDict['pid']
		ppid=retDict['ppid']

		cmdtest="pstree | grep python > " + outPutFile
		retVal=comWrap.comWrap(cmdtest)
		stringGrep = fileFunctions.readFirstLineFile(outPutFile)
		testRet = re.sub("[^0-9]", "", stringGrep)
		self.assertEqual( int(testRet) , int(pid) )
 		
 	def testCreateRaceConditionFileNoFile(self):
		print "  testCreateRaceConditionFileNoFile"
		retDict=systemUtil.getPID()
		processPid=retDict['pid']
		ppid=retDict['ppid']
		#three conditions to check
		#condition 1 = no file
		if fileFunctions.fileExist ( raceConditionOutPutFile ):
			os.unlink(raceConditionOutPutFile)
		retDict2=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		if retDict2['retVal']==0:
			sep=","
			retDict3=dictFunc.fileToDict( raceConditionOutPutFile, sep )
			functionPid=retDict3['pid']
			print "    processPid:   " + processPid
			print "    functionPid:  " + functionPid
			self.assertEqual( int(processPid) , int(functionPid) )
		else:
			print "    createRaceConditionFile function returned an error"
			
 	def testCreateRaceConditionFileFileExistProcessDead(self):
		print "  testCreateRaceConditionFileFileExistProcessDead"
		retDict=systemUtil.getPID()
		processPid=retDict['pid']
		ppid=retDict['ppid']
		#three conditions to check
		#condition 2 = file exists but process is dead
		if fileFunctions.fileExist ( raceConditionOutPutFile ):
			os.unlink(raceConditionOutPutFile)
		
		#create factious process id	
		stringToWrite="pid,9999\n"
		stringToWrite=stringToWrite+"lastFunctionRan,"+str(0)
		fileFunctions.writeToFile(stringToWrite, raceConditionOutPutFile)
		
		retDict2=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		if retDict2['retVal']==0:
			sep=","
			retDict3=dictFunc.fileToDict( raceConditionOutPutFile, sep )
			functionPid=retDict3['pid']
			print "    processPid:   " + processPid
			print "    functionPid:  " + functionPid
			self.assertEqual( int(processPid) , int(functionPid) )
		else:
			print "    createRaceConditionFile function returned an error"
			
	def testCreateRaceConditionFileFileExistProcessDeadFunc(self):
		print "  testCreateRaceConditionFileFileExistProcessDeadFunc"
		retDict=systemUtil.getPID()
		processPid=retDict['pid']
		ppid=retDict['ppid']
		#three conditions to check
		#condition 2 = file exists but process is dead
		if fileFunctions.fileExist ( raceConditionOutPutFile ):
			os.unlink(raceConditionOutPutFile)
		
		#create factious process id	and non zero last function
		stringToWrite="pid,9999\n"
		stringToWrite=stringToWrite+"lastFunctionRan,"+str(2)
		fileFunctions.writeToFile(stringToWrite, raceConditionOutPutFile)
		
		retDict2=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		if retDict2['retVal']==0:
			sep=","
			retDict3=dictFunc.fileToDict( raceConditionOutPutFile, sep )
			functionPid=retDict3['pid']
			lastRunFunc=retDict3['lastFunctionRan']
			print "    lastRunFunc known:   " + str(2)
			print "    lastRunFunc file:    " + lastRunFunc
			self.assertEqual( int(lastRunFunc) , int(2) )
		else:
			print "    createRaceConditionFile function returned an error"
								
 	def testCreateRaceConditionFileFileExistProcessLive(self):
		print "  testCreateRaceConditionFileFileExistProcessLive"
		retDict=systemUtil.getPID()
		processPid=retDict['pid']
		ppid=retDict['ppid']
		#three conditions to check
		#condition 2 = file exists but process is dead
		if fileFunctions.fileExist ( raceConditionOutPutFile ):
			os.unlink(raceConditionOutPutFile)
		
		#create current process id	
		stringToWrite="pid,"+str(processPid)+"\n"
		stringToWrite=stringToWrite+"lastFunctionRan,"+str(0)
		fileFunctions.writeToFile(stringToWrite, raceConditionOutPutFile)
		
		retDict2=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		if retDict2['retVal']==0:
			sep=","
			retDict3=dictFunc.fileToDict( raceConditionOutPutFile, sep )
			functionPid=retDict3['pid']
			print "    processPid:   " + processPid
			print "    functionPid:  " + functionPid
			self.assertEqual( int(processPid) , int(functionPid) )
		else:
			print "    createRaceConditionFile function returned an error"
			self.assertEqual( int(retDict2['retVal']) , int(1) )
			
 	def testUpdateRaceConditionFile	(self):
		print "  testUpdateRaceConditionFile"
		#create race condition file
		retDict2=systemUtil.createRaceConditionFile(raceConditionOutPutFile2)
		key = "lastFunctionRan"
		value = 1
 		systemUtil.updateRaceConditionFile(raceConditionOutPutFile2,key,value)
 		
 		#access value from file
		sep=","
		retDict=dictFunc.fileToDict( raceConditionOutPutFile2, sep )
		print "    value:         " + str(value)
		print "    retDict[key]:  " + str(retDict[key]) 
		self.assertEqual( int(retDict[key]) , int(value) )
	
	def testGetValueInfoBad	(self):
		print "  testGetValueInfoBad"
		#create race condition file
		retDict=systemUtil.createRaceConditionFile(raceConditionOutPutFile2)
		key="test"
		retDict2=systemUtil.getValueInfo(raceConditionOutPutFile2,key)
		retVal=retDict2['retVal']
		comment=retDict2['comment']
		value = 1
		print "    value:         " + str(value)
		print "    retDict[retVal]:  " + str(retVal) 
		print "    comment:  " + comment
		self.assertEqual( int(retVal) , value )
	
	def testGetValueInfoNoFile	(self):
		print "  testGetValueInfoNoFile"
		key="test"
		if fileFunctions.fileExist ( raceConditionOutPutFile2 ):
			os.unlink(raceConditionOutPutFile2)
		retDict2=systemUtil.getValueInfo(raceConditionOutPutFile2,key)
		retVal=retDict2['retVal']
		comment=retDict2['comment']
		value = 1
		print "    value:         " + str(value)
		print "    retDict[retVal]:  " + str(retVal) 
		print "    comment:  " + comment
		self.assertEqual( int(retVal) , value )
		
	def testGetValueInfoGood	(self):
		print "  testGetValueInfoGood"
		#create race condition file
		retDict=systemUtil.createRaceConditionFile(raceConditionOutPutFile3)
		functionString = "0000"
		systemUtil.updateRaceConditionFile(raceConditionOutPutFile3, "functionStatus", functionString)
		key="functionStatus"
		retDict2=systemUtil.getValueInfo(raceConditionOutPutFile3,key)
		retVal=retDict2['retVal']
		result=retDict2['result']
		print "    retDict[retVal]:  " + str(retVal) 
		print "    functionString:   " + functionString
		print "    result:           " + result
		self.assertEqual( functionString , result )
			
	def tearDown(self):
		if fileFunctions.fileExist ( outPutFile ):
			os.unlink(outPutFile)
		if fileFunctions.fileExist ( raceConditionOutPutFile ):
			os.unlink(raceConditionOutPutFile)
		if fileFunctions.fileExist ( raceConditionOutPutFile2 ):
			os.unlink(raceConditionOutPutFile2)
		
if __name__ == '__main__':
    unittest.main()
 