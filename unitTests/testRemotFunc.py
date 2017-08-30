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
listFile = curDir+"/TEMP/listFile.txt"
password="xdr5cft6XDR%CFT^"
import remoteFunc
import fileFunctions
import comWrap

class TestRemoteFunc(unittest.TestCase):
 	
	def setUp(self):
		print ""
		print "setUp"
		print "\t", outputLogFile
		print ""
		if os.path.isfile (outputLogFile):
			os.remove (outputLogFile)

#   	def testPutCkSum(self):
#  		print "testPutCkSum"
# 		#will need to have know output to test this function"
# 		hostname="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remoteDir="testDir"
# 		localFilePath=curDir + "/TEMP/localFile.txt"
# 		retObjFile = fileFunctions.fileCreateWrite(localFilePath, "test, this is a test")
# 		retObj=remoteFunc.putCkSum(hostname, user, localFilePath, remoteDir, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	

  	def testPutSSH(self):
 		print "\ttestPutSSH"
		#will need to have know output to test this function"
		hostname="css-10g.larc.nasa.gov"
		user="jshipman"
		stage="development"
		remoteFilepath="testDir/RemotetestingFile"
		localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile1.png"
		retObj=remoteFunc.putSSH(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
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
			remoteFilepath="testDir/RemotetestingFile" + str(count) + ".png"
			localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile" + str(count) + ".png"
			retObj=remoteFunc.putSSH(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
			result = retObj.getResult()
			retVal = retObj.getRetVal()
			comment = retObj.getComment()
			stdout = retObj.getStdout()
			stderr = retObj.getStderr()
			error = retObj.getError()
			found = retObj.getFound()
			remed = retObj.getRemed()
			print "\t\tresult:  _" + str(result)  + "_"
			print "\t\tretVal:  _" + str(retVal)  + "_"
			print "\t\tcomment: _" + comment + "_"
			print "\t\terror:   _" + error + "_"
			print "\t\tstdout:  _" + stdout + "_"
			print "\t\tstderr:  _" + stderr + "_"
			print "\t\tremed:   _" + remed + "_"
			print "\t\tfound:   _" + str(found) + "_"	
			count = count + 1
			print ""
		
	
				
#   	def testPut(self):
#  		print "\ttestPut"
# 		#will need to have know output to test this function"
# 		hostname="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remoteFilepath="testDir/RemotetestingFile"
# 		localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile1.png"
# 		retObj=remoteFunc.put(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		command = retObj.getCommand()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tCommand:   _" + str(command) + "_"	
# 		
# 		
#   	def testPutMany(self):
#  		print "\ttestPutMany"
# 		stage="development"
# 		count = 1
# 		while (count < 6):
# 			print "\t\tcount:  " + str(count)
# 			hostname="css-10g.larc.nasa.gov"
# 			user="jshipman"
# 			remoteFilepath="testDir/RemotetestingFile" + str(count) + ".png"
# 			localFilePath="/scripts/nearLine/lib/unitTests/TEMP/testFile" + str(count) + ".png"
# 			retObj=remoteFunc.put(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage)
# 			result = retObj.getResult()
# 			retVal = retObj.getRetVal()
# 			comment = retObj.getComment()
# 			stdout = retObj.getStdout()
# 			stderr = retObj.getStderr()
# 			error = retObj.getError()
# 			found = retObj.getFound()
# 			remed = retObj.getRemed()
# 			print "\t\tresult:  _" + str(result)  + "_"
# 			print "\t\tretVal:  _" + str(retVal)  + "_"
# 			print "\t\tcomment: _" + comment + "_"
# 			print "\t\terror:   _" + error + "_"
# 			print "\t\tstdout:  _" + stdout + "_"
# 			print "\t\tstderr:  _" + stderr + "_"
# 			print "\t\tremed:   _" + remed + "_"
# 			print "\t\tfound:   _" + str(found) + "_"	
# 			count = count + 1
# 			print ""
# 		
# 		
#  	def testMkdir(self):
#  		print "testMkdir"
# 		#will need to have know output to test this function"
# 		hostname="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePath="testDir"
# 		retObj=remoteFunc.mkdir(hostname, user, remotePath, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 							
#  	def testStat(self):
#  		print "testStat"
# 		#will need to have know output to test this function"
# 		hostname="css-10g.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		dirFile="test.txt"
# 		retObj=remoteFunc.stat(hostname, user, dirFile, outputLogFile, stage)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		size=result.st_size
# 		print "\t\tsize:  _" + str(size)  + "_"
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	

# 	def testPutFileDirCheck(self):
# 		print "testPutFileDirCheck"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP/txtfile_3_18_9_36"
# 		retObj=remoteFunc.putFileDirCheck(hostname, user, remotePathDst, localPathSrc, stage, password)
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
# 		print "\t\terror:   _" + error + "_"

# 	def testLogonSftp(self):
# 		print "testLogonSftp"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		password=""
# 		stage="development"
# 		retObj=remoteFunc.logonSftp(hostname, user, password)
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

# 	def testMakeDir(self):
# 		print "testMakeDir"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		#password=""
# 		stage="development"
# 		remoteDirPath="/mss/js/jshipman/testDir25"
# 		retObj=remoteFunc.makeDir(hostname, user, remoteDirPath, stage, password)
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

#  	def testCheckSumRemoteCheck(self):
# 		print "testCheckSumRemoteCheck"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1/txtfile_3_18_9_36"
# 		remotePathDstCK="/mss/js/jshipman/archive1/txtfile_3_18_9_36.ck"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP"
# 		delete="no"
# 		retObj=remoteFunc.checkSumRemoteCheck(hostname, user, remotePathDst, remotePathDstCK, localPathSrc, delete, stage, password)
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
# 		print "\t\terror:   _" + error + "_"	

# 	def testGetFile(self):
# 		print "testGetFile"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1/txtfile_3_18_9_36"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP/remoteFile_3_18_12_07"
# 		retObj=remoteFunc.getFile(hostname, user, remotePathDst, localPathSrc, stage, password)
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
# 		print "\t\terror:   _" + error + "_"	

#  	def testPutCheckSum(self):
# 		print "testPutCheckSum"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP/txtfile_3_18_9_36"
# 		retObj=remoteFunc.putCheckSum(hostname, user, remotePathDst, localPathSrc, stage, password)
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
# 		print "\t\terror:   _" + error + "_"	
		
# 	def testPutFile(self):
# 		print "testPutFile"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remotePathDst="/mss/js/jshipman/archive1"
# 		localPathSrc="/scripts/nearLine/lib/unitTests/TEMP/txtfile_3_18_9_36"
# 		retObj=remoteFunc.putFileDir(hostname, user, remotePathDst, localPathSrc, stage, password)
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
# 		print "\t\terror:   _" + error + "_"
# 	
# 	def testGetDirList(self):
# 		print "testGetDirList"
# 		#will need to have know output to test this function"
# # 		hostname="graphix.ndc.nasa.gov"
# # 		user="ladmin"
# # 		stage="development"
# # 		password="i8o9p0I*O(P)"
# # 		remoteDir="/Users/ladmin"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		remoteDir="/mss/js/jshipman"
# 		retObj=remoteFunc.getDirList(hostname, user, remoteDir, listFile, stage, password)
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

# 	def testFileDirStatSSH(self):
#  		print "testFileDirStatSSH"
# 		#will need to have know output to test this function"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		stage="development"
# 		#remotePathDst="archive1/applsrver2.ndc.nasa.gov/readyToArchive/6951_ONeillHerbsandNaturalHealing3232015/6951_ONeillHerbsandNaturalHealing3232015.tar.part-aaa"
# 		remotePathDst="archive1/abac"
# 		retObj=remoteFunc.fileDirStatSSH( remotePathDst, hostname, user, stage)
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
			 
#  	def testFileDirStat(self):
#  		print "testFileDirStat"
# 		#will need to have know output to test this function"
# 		hostname="css.larc.nasa.gov"
# 		user="jshipman"
# 		#password=""
# 		stage="development"
# 		remotePathDst="archive1/applsrver2.ndc.nasa.gov/readyToArchive/6951_ONeillHerbsandNaturalHealing3232015/6951_ONeillHerbsandNaturalHealing3232015.tar.part-aaa"
# 		retObj=remoteFunc.fileDirStat(hostname, user, remotePathDst, stage, password)
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
		
if __name__ == '__main__':
    unittest.main()
 