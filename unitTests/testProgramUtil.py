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
raceConditionOutPutFile = curDir+"/raceConditionOutPutFile.txt"
import programUtil
import comWrap
import fileFunctions
import dictFunc
import systemUtil

class TestProgramUtil(unittest.TestCase):
 	print "Tests for `systemUtil.py`."
 	
	def setUp(self):
		pass
 
	def testFunctionStatusLengthBad(self):
		print "  testFunctionStatusLengthBad"
		statusString="010101"
		index=7
		retDict=programUtil.functionStatus(statusString,index)
		retVal=retDict['retVal']
		self.assertEqual( int(1) , int(retVal) )
 		
	def testFunctionStatusLengthGood(self):
		print "  testFunctionStatusLengthGood"
		statusString="010101"
		index=5
		retDict=programUtil.functionStatus(statusString,index)
		retVal=retDict['retVal']
		self.assertEqual( int(0) , int(retVal) )	
		
	def testFunctionStatusIndexValue(self):
		print "  testFunctionStatusIndexValue"
		statusString="010101"
		index=5
		retDict=programUtil.functionStatus(statusString,index)
		result=retDict['result']
		self.assertEqual( int(1) , int(result) )
		
	def testChangeFunctionStatus(self):
		print "  testChangeFunctionStatus"
		statusString="010101"
		index=5
		retDict=programUtil.changeFunctionStatus(statusString,index,0)
		result=retDict['result']
		self.assertEqual( str("010100") , str(result) )
		
	def testFunctionStatusWrap(self):
		def printOut ( text, text2 ):
			print "text:   " + text
			print "text2:  " + text2
		print "  testFunctionStatusWrap"
		#create race condition file
		retDict=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		functionString = "0000"
		key = "functionStatus"
		systemUtil.updateRaceConditionFile(raceConditionOutPutFile, key, functionString)	
		indexForString = 0
		programUtil.functionStatusWrap ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1000"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )
		indexForString = 1
		programUtil.functionStatusWrap ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1100"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )
		indexForString = 3
		programUtil.functionStatusWrap ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1101"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )

	def testFunctionStatusWrapReturn(self):
		print "  testFunctionStatusWrap"
		def printOut ( text, text2 ):
			print "    printOut func "
			print "      text:   " + text
			print "      text2:  " + text2
		
		#create race condition file
		retDict=systemUtil.createRaceConditionFile(raceConditionOutPutFile)
		functionString = "0000"
		key = "functionStatus"
		systemUtil.updateRaceConditionFile(raceConditionOutPutFile, key, functionString)	
		indexForString = 0
		retDict=programUtil.functionStatusWrapReturn ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		print retDict['comments']
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1000"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )
		indexForString = 1
		retDict=programUtil.functionStatusWrapReturn ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		print retDict['comments']
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1100"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )
		indexForString = 3
		retDict=programUtil.functionStatusWrapReturn ( raceConditionOutPutFile, key, indexForString, printOut, "testing ",  "parameters ")
		print retDict['comments']
		dict=dictFunc.fileToDict(raceConditionOutPutFile,",")
		funcStringFromFile = dict[key]
		funcStringKnown = "1101"
		self.assertEqual( str(funcStringFromFile) , str(funcStringKnown) )
if __name__ == '__main__':
    unittest.main()
 