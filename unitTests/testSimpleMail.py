#!/usr/bin/python
import unittest
import inspect
import os, sys
import datetime
import time
import shutil
curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()

import simpleMail

class simpleMailTestCase(unittest.TestCase):
	print "Tests for `simpleMail.py`."

	def setUp(self):
		print "\tSetup"	

	def testShortMessage2(self):
		print "\tTestShortMessage2"
		mailList = {}
		from_addr = "ladmin@testing.com"
		to_addr="jeffery.l.shipman@nasa.gov"
		message = "message - testing simple mail 2"
		subject = "subject - testing simple mail 2"
		mailList['from_addr'] = from_addr
		mailList['to_addr'] = to_addr 
		mailList['message'] = message
		mailList['subject'] = subject
		retObj=simpleMail.shortMessage2( mailList )
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
		print "\t\tcomment:  _" + comment
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"
		print "\t\tError:   _" + error + "_"


	def tearDown(self):
		print "\ttearDown"
