#!/usr/bin/python
import unittest, inspect, os, sys
curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
dirName2 = os.path.dirname(dirName)
libPath = dirName2 + "/lib"
sys.path.append(libPath)
import unittest
import archiveFunc
 
class TestArchiveFunc(unittest.TestCase):
 	print "Test Archive Fucntions"
	def setUp(self):
		print "#############################################"
		print "setUp" 
		
	def testTarFunction(self):
		print "\ttestTarFunction"
		tarPath  = "/scripts/nearLine/lib/unitTests/tar/testFile.tar"
		itemPath = "/scripts/nearLine/lib/unitTests/temp/testFile.png"
		curDir = os.getcwd()
		dir = os.path.dirname(itemPath)
		base = os.path.basename(itemPath)
		os.chdir(dir)
		
		retObj = archiveFunc.tarFunction( tarPath, base )
		
		os.chdir(curDir)
		
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tcommand: _" + command + "_"	
		print "\t\terror:   _" + error + "_"	

	def testCreateArchiveSplit(self):
		print "\ttestcreateArchiveSplit"
		pathArchiveFile  = "/scripts/nearLine/lib/unitTests/tar/testFile.tar"
		pathSplitFile = "/scripts/nearLine/lib/unitTests/split/testFile.tar.part-"
		amount = 107374182400
		retObj = archiveFunc.createArchiveSplit( amount, pathArchiveFile, pathSplitFile )
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tcommand: _" + command + "_"
		print "\t\terror:   _" + error + "_"	

	def testTarSplitWrap(self):
		print "\ttestTarSplitWrap"
		archiveNameFull  = "/scripts/nearLine/lib/unitTests/tar/testFile.tar"
		locationPathFull = "/scripts/nearLine/lib/unitTests/temp/testFile.png"
		pathSplitFile = "/scripts/nearLine/lib/unitTests/split/testFile.tar.part-"
		amount = 107374182400
		paraList = [archiveNameFull, locationPathFull, pathSplitFile, amount]
		retObj = archiveFunc.tarSplitWrap( paraList )
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		error = retObj.getError()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tcommand: _" + command + "_"	
		print "\t\terror:   _" + error + "_"	


	def tearDown(self):
		print "tearDown" 
		print "#############################################"
		print ""
 
      
if __name__ == '__main__':
    unittest.main()