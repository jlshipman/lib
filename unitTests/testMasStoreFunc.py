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
outputLogFile = curDir+"/TEMP/outputLogFile.txt"
import masStoreFunc
import fileFunctions
import comWrap

class TestMasStoreFunc(unittest.TestCase):
 	
	def setUp(self):
		print ""
		print "setUp"
		print "\t", outputLogFile
		print ""
		if os.path.isfile (outputLogFile):
			os.remove (outputLogFile)

 	def testPutSSH(self):
 		print "\ttestPutSSH"
		#will need to have know output to test this function"
		hostname="css-10g.larc.nasa.gov"
		user="jshipman"
		stage="development"
		#remoteFilepath="testDir/RemotetestingFile"
		#localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile1"
		remoteFilepath="testDir/screen1.png"
		localFilePath="/scripts/nearLine/lib/unitTests/TEMP/screen1.png"
		retObj=masStoreFunc.putSSH(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		error = retObj.getError()
		found = retObj.getFound()
		remed = retObj.getRemed()
		command = retObj.getCommand()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\terror:   _" + error + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"
		print "\t\tCommand:   _" + str(command) + "_"

  	def testPutSSHMany(self):
 		print "\ttestPutSSHMany"
		stage="development"
		count = 1
		while (count < 6):
			print "\t\tcount:  " + str(count)
			hostname="css-10g.larc.nasa.gov"
			user="jshipman"
			remoteFilepath="testDir/RemotetestingFile" + str(count)
			localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile" + str(count)
			remoteFilepath="testDir/screen" + str(count) + ".png"
			localFilePath="/scripts/nearLine/lib/unitTests/TEMP/screen" + str(count) + ".png"
			retObj=masStoreFunc.putSSH(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
			result = retObj.getResult()
			retVal = retObj.getRetVal()
			comment = retObj.getComment()
			stdout = retObj.getStdout()
			stderr = retObj.getStderr()
			error = retObj.getError()
			found = retObj.getFound()
			remed = retObj.getRemed()
			command = retObj.getCommand()
			print "\t\t\tresult:  _" + str(result)  + "_"
			print "\t\t\tretVal:  _" + str(retVal)  + "_"
			print "\t\t\tcomment: _" + comment + "_"
			print "\t\t\terror:   _" + error + "_"
			print "\t\t\tstdout:  _" + stdout + "_"
			print "\t\t\tstderr:  _" + stderr + "_"
			print "\t\t\tremed:   _" + remed + "_"
			print "\t\t\tfound:   _" + str(found) + "_"	
			print "\t\t\tcommand: _" + str(command) + "_"	
			count = count + 1
			print ""
			
# 	def testCheckSum(self):
#  		print "testCheckSum"
# 		#will need to have know output to test this function"
# 		remoteHost="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remoteDirFile="test.txt"
# 		retObj=masStoreFunc.checkSum(remoteHost, user, remoteDirFile, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		
# 	def testCheckTape(self):
#  		print "testCheckTape"
# 		#will need to have know output to test this function"
# 		remoteHost="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remoteDirFile="test.txt"
# 		retObj=masStoreFunc.checkTape(remoteHost, user, remoteDirFile, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 		print "\t\terror:   _" + str(error) + "_"	
					
if __name__ == '__main__':
    unittest.main()
 