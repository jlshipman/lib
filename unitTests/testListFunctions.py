#!/usr/bin/python
import unittest
import os, sys
import collections

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
listSetA = ['A', 'B','C', 'D', 'E']
listSetB = ['E', 'F', 'G', 'H', 'I']
listSetLeftJoin = ['A', 'B','C', 'D']
stringTest = "many   fancy word \nhello    \thi"
stringTest2 = "many$fancy$wor$hello$hi"
testResult = ['many', 'fancy', 'word', 'hello', 'hi']		
import listFunctions

class listFunctionsTestCase(unittest.TestCase):
	print "Tests for `listFunction.py`."
	
	def setUp(self):
		pass

	def testLlolLolSetDiff(self):
		print "testLlolLolSetDiff"
		index = 0
		lol = [[1, 2, 3], [2, 3, 4]]
		lol2 = [[2, 3, 4], [3, 4, 5]]
		retObj = listFunctions.lolLolSetDiff(lol, index, lol2, index)
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
		
	def testLolLolComp(self):
		print "testLolLolComp"
		sep="#"
		index=0
		index2=0
		filePath="/scripts/compare/lib/unitTests/LIST/testList.txt"
		resList1 = listFunctions.listofListFromFile (filePath, sep)
		filePath="/scripts/compare/lib/unitTests/LIST/testList2.txt"
		resList2 = listFunctions.listofListFromFile (filePath, sep)
		resultDict=listFunctions.lolLolComp(resList1, index, resList2, index2)
		foundList=resultDict['foundList']
		notFoundList=resultDict['notFoundList']
		print "\tFound List"
		for item in foundList:
			print "\t\t"+ str(item)
		print "\tNot Found List"
		for item in notFoundList:
			print "\t\t"+ str(item)	
				
	def testListofListFromFile(self):
		print "testListofListFromFile"
		sep="#"
		filePath="/scripts/compare/lib/unitTests/LIST/testList.txt"
		resList = listFunctions.listofListFromFile (filePath, sep)
		for item in resList:
			print item
			
	def testStringToListWhitespace(self):
		print "testStringToListWhitespace"
		resList = listFunctions.stringToList(stringTest)
		resutltDict = listFunctions.listComp(resList, testResult)
		notFoundList = resutltDict['notFoundList']
	 	
	 	print "list from function - notFoundList"
		for item in notFoundList:
			print "_" + item + "_" 
	 			
	 	if set(resList) == set(testResult):
	 		print "list are the same"
	 		
	 	else:
	 		print "list are not the same"
		
	def testListCompIntersection(self):	
		print "testListCompFound"
	 	resutltDict = listFunctions.listComp(listSetA, listSetB)
	 	c3 = set(listSetA).intersection( set(listSetB) )
	 	foundList = resutltDict['foundList']
	 	
	 	print "list from function - foundlist"
		for item in foundList:
			print "_" + item + "_" 
		
		print "list from check function - lambda"
		for item in c3:
			print "_" + item + "_" 
	 			
	 	if set(foundList) == set(c3):
	 		print "list are the same"
	 		
	 	else:
	 		print "list are not the same"
	 		
	def testListCompNotFoundLeftJoin(self):	
		print "testListCompNotFoundRightJoin"
	 	resutltDict = listFunctions.listComp(listSetA, listSetB)
	 	notFoundList = resutltDict['notFoundList']
	 	
	 	print "list from function - notFoundList"
		for item in notFoundList:
			print "_" + item + "_" 
		
		print "list from check set  - listSetLeftJoin"
		for item in listSetLeftJoin:
			print "_" + item + "_" 
	 			
	 	if set(notFoundList) == set(listSetLeftJoin):
	 		print "list are the same"
	 		
	 	else:
	 		print "list are not the same"
	 		
	def tearDown(self):
		pass


if __name__ == '__main__':
    unittest.main()