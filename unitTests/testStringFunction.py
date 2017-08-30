#!/usr/bin/python
import unittest, inspect, os, sys
curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
dirName2 = os.path.dirname(dirName)
libPath = dirName2 + "/lib"
sys.path.append(libPath)
import stringFunctions
import funcReturn

class TestStrimgFunction(unittest.TestCase):
	print "TestStrimgFunction"
 
	def setUp(self):
		print "\t#############################################"
		print "\tsetUp" 

	def testStrFind(self):
		print "\t\ttestStrFind"
		haystack = "aaaaaaaaazAAAAAAAAAA"
		needle = "z"	
 		retObj = stringFunctions.strFind( haystack, needle )
 		Name = retObj.getName()
 		Comment = retObj.getComment()
 		retVal = retObj.getRetVal()
 		print "\t\t\tName:     " + Name
 		print "\t\t\tComment:  " + Comment
 		print "\t\t\tretVal:   " +  str(retVal)
 		
	def tearDown(self):
		print "\ttearDown" 
		print "\t#############################################"
		print ""
    
if __name__ == '__main__':
    unittest.main()