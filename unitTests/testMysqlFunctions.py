#!/usr/bin/python
import unittest
import inspect
import os, sys
import datetime
import time
import shutil
curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
libPath = os.path.dirname(curDir)
sys.path.append(libPath)
print "libPath:  " + libPath

libPhotoPath = os.path.dirname(libPath) +  "/libPhoto"
sys.path.append(libPhotoPath)
print "libPhotoPath:  " + libPhotoPath

import mysqlFunctions
import photoFunctions

class TestMysqlFunctions(unittest.TestCase):
	print "Tests for `mysqlFunctions.py`."

	def setUp(self):
		print "#############################################"
		print "setUp" 


	def testShowQuery(self):
		print "\tTestShowQuery"
		query = """INSERT INTO P_L(fileName, lYear, lSequence, prefix,  timeModifiy, timeCreated, raw, rawDVD) 
		VALUES (%s , %s , %s , %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s )"""
		stringArray = ["%s" , "%s" , "%s" , "%s", "%s", "%s"]
		searchArray =  ["a" , "b" , "c" , "d" , "e", "f"]
		retObj = mysqlFunctions.showQuery ( query, stringArray, searchArray)
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
		print "\t\tcomment:  _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"
		print "\t\tError:   _" + error + "_"
		
	def testExportCSV(self):
		print "\tTestExportCSV"
		stage = "developmentMarvin"
		year = 1923
		retObjConn = photoFunctions.photoConnectMysql2(stage)
		conn = retObjConn.getResult()
		retObjPhtoto = photoFunctions.photoYearRecordsExport (conn, year)
		data = retObjPhtoto.getResult()
		exportFile = "/scripts/photoProcess/lib/unitTests/exportFile.txt"
		retObj=mysqlFunctions.exportCSV (data, exportFile)
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		error = retObj.getError()
		print "\t\tresult:  _" + str(result)  + "_"
 		print "\t\tsize of result list   _" + str(len(result))  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment:  _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"
		print "\t\tError:   _" + error + "_"
		print "\t\tdata:   _" + str(data) + "_"


	def tearDown(self):
		print "tearDown" 
		print "#############################################"
		print ""
		
if __name__ == '__main__':
    unittest.main()
