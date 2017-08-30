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

#dirSize
fp = curDir+"/testDir"
structure= [ 
fp+"/file/file.x", 
fp+"/another/file/file.y", 
fp+"/other/path/file.z"
]

#listFilesSuffix
fp2 = curDir+"/testDir2/dir/"
structure2= [ 
fp2+"file1.txt", 
fp2+"file2.txt",
fp2+"file3.txt"]

import directory

class directoryTestCase(unittest.TestCase):
	print "Tests for `directory.py`."

	def setUp(self):
		print "\tSetup"	
# 		#DirSize setup
# 		for p in structure:
# 			path, file = os.path.split( p )
# 			if not os.path.exists (path):
# 				try:
# 					os.makedirs( path )
# 				except OSError:
# 					print "could not created directory:  " + path
# 			with open( p, "w" ) as f:
# 				f.write( "Dummy Data" )
# 					
# 		#listFilesSuffix setup
# 		for p in structure2:
# 			path, file = os.path.split( p )
# 			if not os.path.exists (path):
# 				try:
# 					os.makedirs( path )
# 				except OSError:
# 					print "could not created directory:  " + path
# 			with open( p, "w" ) as f:
# 				f.write( "Dummy Data" )
# 
	def testListFilesSuffixSortCreate(self):
		print "\ttestListFilesSuffixSortCreate"
		dirPath = "/Volumes/photoRepository/source/"
		retObj=directory.listFilesSuffixSortCreate( dirPath, "ck" )
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		found = retObj.getFound()
		remed = retObj.getRemed()
		error = retObj.getError()
 		for r in result:
 			print r
		print "\t\tsize of result list   _" + str(len(result))  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment:  _" + comment + "_"
		print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"
		print "\t\tError:   _" + error + "_"
		

# 	def testDeleteDirContents(self):
# 		print "\ttestDeleteDirContents"
# 		dirPath = "/scripts/photoProcess/lib/unitTests/testDir"
# 		retObj=directory.deleteDirContents(dirPath)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
#  		print "\t\size of result list   _" + str(len(result))  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tError:   _" + error + "_"
# 
# 
# 	def testMoveDirContents(self):
# 		print "\ttestMoveDirContents"
# 		src = "/scripts/photoProcess/lib/unitTests/testDir"
# 		dst = "/scripts/photoProcess/lib/unitTests/testDirDst"
# 		retObj=directory.moveDirContents(src, dst)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
#  		print "\t\size of result list   _" + str(len(result))  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tError:   _" + error + "_"
# 
# 
# 	def testListFilesSuffixNoDups2(self):
# 		print "\ttestListFilesSuffixNoDups2"
# 		dirPath = "/Volumes/photoRepository/testing"
# 		retObj=directory.listFilesSuffixNoDups2( dirPath, "tif" )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		error = retObj.getError()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\size of result list   _" + str(len(result))  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tError:   _" + error + "_"
# 
# 	def testMakeDirectoryObj(self):
# 		print "\ttestMakeDirectoryObj"
# 		dirPath = "/Volumes/photoRepository/temp/mastered/1956/pic"
# 		retObj=directory.makeDirectoryObj( dirPath )
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
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tError:   _" + error + "_"

# 	def testMvDir(self):
# 		print "\ttestMvDir"
# 		source = "/Volumes/videoSAN/Temp/test/8005_KristynDamadeo_SAGEIIIMediaTraining_040715"
# 		dest = "/Volumes/videoSAN/Temp/test/8005_KristynDamadeoSAGEIIIMediaTraining_040715"
# 		retObj=directory.mvDir( source, dest )
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
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		print "\t\tError:   _" + error + "_"
# 
#  	def testSetAttributes(self):	
# 		print "\ttestSetAttributes"
# 		dirPath = "/Volumes/videoSAN/p2_SD"
# 		priv="775"
# 		own = "ladmin"
# 		group = "videoeditors"
# 		retObj=directory.setAttributes( dirPath, own, group, priv )
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print comment
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"
# 		
# 	def testSetPrivilege(self):	
# 		print "\ttestSetPrivilege"
# 		dirPath = "/Volumes/videoSAN/p2_SD"
# 		priv="775"
# 		retObj=directory.setPrivilege(dirPath, priv)
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
# 		
# 	def testSetGroupOwner(self):	
# 		print "\ttestSetGroupOwner"
# 		dirPath = "/Volumes/videoSAN/p2_SD"
# 		own = "ladmin"
# 		group = "videoeditors"
# 		retObj=directory.setGroupOwner(dirPath, own, group)
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
# 		
# 	def testSetToUnLock(self):	
# 		print "\ttestSetToUnLock"
# 		dirPath = "/Volumes/videoSAN/p2_SD"
# 		retObj=directory.setToUnLock(dirPath)
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
# 			
# 	def testListFilesSuffixNoDups(self):	
# 		print "\ttestListFilesSuffixNoDups"
# 		suffix="tif"
# 		dirPath="/scripts/compare/lib/unitTests/images"
# 		resultdict=directory.listFilesSuffixNoDups(dirPath, suffix)
# 		print "\t\tresultdict['resultList']"
# 		print resultdict['resultList']	
# 		print "\t\tresultdict['resultListFullPath']"
# 		print resultdict['resultListFullPath']		
# 		print "\t\tresultdict['resultListBoth']"	
# 		print resultdict['resultListBoth']	
# 		print "\t\tresultdict['resultListMetaData']"
# 		print resultdict['resultListMetaData']		
# 		print "\t\tresultdict['amount']"	
# 		print resultdict['amount']	
# 		
# 	def testDirSize(self):
# 		print "\ttestDirSize"
# 		pathSizeBytes = os.path.getsize(fp)
# 		size=directory.dirSize(fp)
# 		self.assertEqual(pathSizeBytes, size)
# 		
# 	def testListFilesSuffix(self):
# 		print "\ttestListFilesSuffix"
# 		suffix = ".txt"
# 		resultDict=directory.listFilesSuffix (fp2, suffix)
# 		resultSize = resultDict['amount']
# 		size = len(structure)
# 		self.assertEqual(resultSize, size)
# 	
# 	def testFindDirectory(self):
# 		print "  testFindDirectory"
# 		#based on file path creations from structure
# 		#directory "path" should be of depth 2
# 		findDir = "path"
# 		lookToDepth = 2
# 		knownDepth = 2
# 		retDict=directory.findDirectory(fp, findDir, lookToDepth)
# 		retVal=retDict['retVal']
# 		depth=retDict['depth']
# 		self.assertEqual(knownDepth, depth)
# 		
# 	def testCountFilesWithPrefix(self):
# 		print "\ttestListFilesSuffix"
# 		prefix = "file"
# 		#based on file path creations from structure2
# 		#number of files with prefix "file" is 3
# 		knownAmount= 3
# 		retVal = directory.countFilesWithPrefix(fp2, prefix)
# 		self.assertEqual(knownAmount, retVal)
# 	
# 	def testCountFiles(self):
# 		print "\ttestCountFiles"
# 		#based on file path creations from structure2
# 		#number of files with in the directory is 3
# 		knownAmount= 3
# 		retVal = directory.countFiles(fp2)
# 		self.assertEqual(knownAmount, retVal)
			
	def tearDown(self):
		print "\ttearDown"
# 		#DirSize tearDown
# 		shutil.rmtree(fp)
# 		
# 		#listFilesSuffix tearDown
# 		shutil.rmtree(fp2)
