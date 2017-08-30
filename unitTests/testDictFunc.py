#!/usr/bin/python
import unittest
import os, sys
import filecmp

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
outputtestFileToDict = curDir+"/outputtestFileToDict.txt"
outputtestFileToDictSub = curDir+"/outputtestFileToDictSub.txt"
outPutFile = curDir+"/output.txt"
outPutFile2 = curDir+"/output2.txt"
import dictFunc
import fileFunctions

class dictFuncTestCase(unittest.TestCase):
	print "Tests for `dictFun.py`."
	
	def setUp(self):
		pass
		
		
	def testSetPrivilege(self):
		print "  testFileToDict"
		
		
# 	def testFileToDict(self):
# 		print "  testFileToDict"
# 		fo = open(outputtestFileToDict, "w")
# 		fo.write("key1 value1\n")
# 		fo.write("key2 value2\n")
# 		fo.write("key3 value3\n")
# 		fo.close()
# 		dict = {}
# 		dict['key1']="value1"
# 		dict['key2']="value2"
# 		dict['key3']="value3"
# 		retDict = dictFunc.fileToDict(outputtestFileToDict, " ")
# 		try:
# 			os.unlink(outputtestFileToDict)
# 		except:
# 			print "  unable to delete " + outputtestFileToDict
# 		shared_items = set(retDict.items()) & set(dict.items())
# 		print "    length of created dict:  " + str(len(dict))
# 		print "    length of read from file dict:  " + str(len(retDict))
# 		print "    length of shared items:  " + str(len(shared_items))
# 		self.assertEqual(len(dict), len(retDict), len(shared_items))
# 
# 	def testFileToDictSub(self):
# 		print "  testFileToDictSub"
# 		fo = open(outputtestFileToDictSub, "w")
# 		fo.write("key1 value1\n")
# 		fo.write("key2 key1 value2\n")
# 		fo.write("key3 value3\n")
# 		fo.close()
# 		dict = {}
# 		dict['key1']="value1"
# 		dict['key2']="value1value2"
# 		dict['key3']="value3"
# 		retDict = dictFunc.fileToDictSub(outputtestFileToDictSub, " ")
# 		try:
# 			os.unlink(outputtestFileToDictSub)
# 		except:
# 			print "  unable to delete " + outputtestFileToDictSub
# 		shared_items = set(retDict.items()) & set(dict.items())
# 		print "    length of created dict:  " + str(len(dict))
# 		print "    length of read from file dict:  " + str(len(retDict))
# 		print "    length of shared items:  " + str(len(shared_items))
# 		self.assertEqual(len(dict), len(retDict), len(shared_items))
# 		
# 	def testDictToFile(self):
# 		print "  testFileToDictSub"
# 		fo = open(outPutFile, "w")
# 		fo.write("key1,value1\n")
# 		fo.write("key2,value2\n")
# 		fo.write("key3,value3\n")
# 		fo.close()
# 		
# 		
# 		dict = {}
# 		dict['key1']="value1"
# 		dict['key2']="value2"
# 		dict['key3']="value3"
# 		
# 		sep=","
# 		retDict = dictFunc.dictToFile(dict, outPutFile2, sep)
# 		retVal = filecmp.cmp(outPutFile, outPutFile2, shallow=False) 
# 		#print "retVal:  " + str(retVal)
# 		desiredVal = True 
# 		#print "desiredVal:  " + str(desiredVal)
# 		self.assertEqual(retVal, desiredVal)
# 
# 	def tearDown(self):
# #		pass
# 		if fileFunctions.fileExist ( outPutFile ):
# 			os.unlink(outPutFile)
# 		if fileFunctions.fileExist ( outPutFile2 ):
# 			os.unlink(outPutFile2)

if __name__ == '__main__':
    unittest.main()