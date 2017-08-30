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
import mainTest


class TestMainTest(unittest.TestCase):
 	print "Tests for `systemUtil.py`."
 	
	def setUp(self):
		pass
 
	def testMainTest(self):
		print "  testMainTest"
		statusString="1011"
		retVal=mainTest.testMain()
		print "    statusString:  " + statusString
		print "    retVal:        " + str(retVal)
		self.assertEqual( statusString , retVal )
 			

		
if __name__ == '__main__':
    unittest.main()
 