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


import fileSize

class fileSizeTest(unittest.TestCase):
	print "Tests for `fileSiz.py`."

	def setUp(self):
		print "\tSetup"	
				
	def testFile_Size(self):	
		print "\ttestFile_Size"
		amount = 1324124312341234123
		retObj=fileSize.file_Size( amount )
		size=retObj.getSize()
		print "\t\tsize:  _" + str(size)  + "_"
	
	def testGetGB(self):	
		print "\ttestGetGB"
		amount = 1324124312341234123
		unit = 'bytes'
		retObj=fileSize.file_Size( amount )
		gb=retObj.getGB()
		size=retObj.getSize()
		print "\t\tsize:  _" + str(size)  + "_"
		print "\t\tgb:  _" + str(gb)  + "_"
	
	def tearDown(self):
		print "\ttearDown"

