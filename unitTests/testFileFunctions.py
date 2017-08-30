#!/usr/bin/python	
import unittest
import os, sys

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
print "curDir:  " + curDir
dirPath=curDir + "/TEMP"
print "dirPath:  " + dirPath
sample=dirPath + "/sample.txt"
fileToCheckSum = sample
creatFile = dirPath + "/createFile.txt"
import fileFunctions

class TestFileFunction(unittest.TestCase):
 	print "Tests for `fileFunction.py`."
 	
	def setUp(self):
		print "setUp"

	def testFindRemoveString(self):
		print "\tTestFindRemoveString"	
		filePath="/scripts/compare/lib/unitTests/fileListTest.txt"
		string="c"
		retObj = fileFunctions.findRemoveString(string, filePath)
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		error = retObj.getError()

		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\terror:  _" + str(error)  + "_"

# 	def testFileStatsNoGroupsSpacesFromString(self):
# 		fileLine ="drwxrw----     2 bpoythre       3584  Mar 29 15:35 RAW DVD 0181 BURNED"
# 		print "\ttestFileStatsNoGroupsSpacesFromString"	
# 		print "\t\tfileLine: _" + fileLine + "_"
# 		retObj = fileFunctions.fileStatsNoGroupsSpacesFromString(fileLine)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 
# 	def testRemoveBadChar(self):
# 		print "\ttestRemoveBadChar"	
# 		string="Shipman#120997433#Husch"
# 		retString = fileFunctions.removeBadChar(string)
# 		print "\t\tretString:  _" + str(retString)  + "_"
# 		
# 	def testFindStringTrue(self):
# 		print "\ttestFindStringTrue"	
# 		filePath=sample
# 		string="second output"
# 		retObj = fileFunctions.findString(string, filePath)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 
# 	def testFindStringFalse(self):
# 		print "\ttestFindStringFalse"	
# 		filePath=sample
# 		string="third output"
# 		retObj = fileFunctions.findString(string, filePath)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 
# 
# 	def testConvertToBytes2(self):
# 		print "\ttestConvertToBytes2"	
# 		retObj = fileFunctions.convertToBytes2(2, "TB")
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		
# 	def testFileCreateWrite(self):
# 		print "\ttestFileCreateWrite"	
# 		localFilePath=curDir + "/TEMP/localFile.txt"
# 		retObj = fileFunctions.fileCreateWrite(localFilePath, "testing create file write function")
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
		
# 	def testCheckSumObj(self):
# 		print "\ttestCheckSumObj"	
# 		print "\t\tfileToCheckSum:  " + fileToCheckSum
# 		retObj = fileFunctions.checkSumObj(fileToCheckSum)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
		
		
# 	def testPrintFile(self):
# 		print "\ttestPrintFile"	
# 		fileFunctions.printFile(sample)
# 			
#  	def testCreateFiles(self):
# 		print "\ttestCreateFiles"	
# 		amount=7
# 		base="testing"
# 		suffix=".tif"
# 		retDict=fileFunctions.createFiles(dirPath, amount, base, suffix)
# 		retVal=retDict['retVal']
# 		knowCount= 0
# 		for the_file in os.listdir(dirPath):
# 			file_path = os.path.join(dirPath, the_file)
# 			if os.path.isfile(file_path) and the_file.endswith(suffix):
# 				knowCount = knowCount + 1
# 		self.assertEqual( int(knowCount) , int(amount) )
# 		
# 	def testDeleteFiles(self):
# 		print "\tdeleteFiles"	
# 		suffix=".tif"
# 		correctAnswer=0
# 		retDict=fileFunctions.deleteFiles(dirPath, suffix)
# 		retVal=retDict['retVal']
# 		programCount= 0
# 		for the_file in os.listdir(dirPath):
# 			file_path = os.path.join(dirPath, the_file)
# 			if os.path.isfile(file_path) and the_file.endswith(suffix):
# 				programCount = programCount + 1
# 		self.assertEqual( int(programCount) , int(correctAnswer) )
	
	def tearDown(self):
		print "tearDown"
# 		for the_file in os.listdir(dirPath):
# 			file_path = os.path.join(dirPath, the_file)
# 			try:
# 				if os.path.isfile(file_path):
# 					os.unlink(file_path)
# 			except Exception, e:
# 				print e
		
 		
if __name__ == '__main__':
    unittest.main()
 
