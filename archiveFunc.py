import subprocess, os, sys
import optparse
from subprocess import call
sys.path.append('lib')
import string
import fileFunctions
import listFunctions
import timeFunc
import datetime 
import time
import comWrap
import tarfile
import directory
import funcReturn
import os

def createArchiveSplit  ( amount, pathArchiveFile, pathSplitFile ):
	#split -a 3 -b $splitAmount ${tempTar}$tarFile "${tempSplit}$tarFile.part-"
	command = "/usr/bin/split -a 3 -b " + str(amount) + " " + pathArchiveFile + " " + pathSplitFile
	retObj = comWrap.comWrapString(command)
	retObj.setName("createArchiveSplit")	
	return retObj
	
def tarFunction ( tarPath, itemPath ):
	#gnutar -cvf  $tempTar$tarFile "$local_dir"		
	command = "/usr/bin/gnutar -cf " + tarPath  + " " + itemPath
	retObj = comWrap.comWrapString(command)
	retObj.setName("tarFunction")
	return retObj


def tarSplitWrap (paraList):
	retObj = funcReturn.funcReturn('archiveSplitWrap')
	dt1=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
	archiveNameFull =  paraList [0]
	locationPathFull =  paraList [1]
	splitFull =  paraList [2]
	Amount =  paraList [3]
	dict = {}
	dict['dt1']=dt1
	dict['archiveNameFull']=archiveNameFull
	dict['locationPathFull']=locationPathFull
	dict['splitFull']=splitFull
	dict['Amount']=Amount
	
	curDir = os.getcwd()
	dir = os.path.dirname(locationPathFull)
	base = os.path.basename(locationPathFull)
	os.chdir(dir)
	
	retObjTar = tarFunction (archiveNameFull, base)
	retVal = retObjTar.getRetVal()
	if retVal == 1:
		retObj.setRetVal(1)
		retObj.setError ("tarFunction  \nstdError:  " +  retObjTar.getStderr() + "\nstdOut:  "+  retObjTar.getStdout())
		return retObj
		
	os.chdir(curDir)
	
		
	size=fileFunctions.fileSize(archiveNameFull)
	if size == -1:
		retObj.setError ("fileSize:  could not stat file :  " + archiveNameFull)
		return retObj
		
	
	
 	retObjSplit = createArchiveSplit (Amount, archiveNameFull, splitFull)
 	retVal = retObjSplit.getRetVal()
 	if retVal == 1:
 		retObj.setError ("tarFunction  \nstdError:  " +  retObjSplit.getStderr() + "\nstdOut:  "+  retObjSplit.getStdout())
 		return retObj
 		
 	dt2=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
 	date1 = datetime.datetime.strptime(dt1, "%Y-%b-%d-%H:%M:%S") 
 	date2 = datetime.datetime.strptime(dt2, "%Y-%b-%d-%H:%M:%S") 
   	tdelta=(date2 - date1)
 	delta_seconds = (tdelta.days * 60 * 60 * 24) + tdelta.seconds + ((tdelta.microseconds + 500000) / 1000000) 
 	seconds = delta_seconds
 	
  	if retVal == 0:
  		if (os.path.exists ( archiveNameFull )): 
 			os.remove(archiveNameFull)
 	resDict = {}
	resDict['size']=size
	resDict['seconds']=seconds 
	retObj.setRetVal(0)	
	retObj.setResult(resDict)
	return retObj
	
def archivePrep (lg, filePath, tempSplit):
	dict = {'function' : 'archivePrep'}
	
	#read dir
	path = filePath.rstrip()		
	
	#get only directory to tar
	baseOrig = os.path.basename(path) 
	
	#get one directory up
	dirUpFull = os.path.dirname(path)
	
	dirUp =  os.path.basename(dirUpFull)	
	tempSplitFull = tempSplit + dirUp
	
	retDict = directory.makeDirectoryBash(tempSplitFull)
	comment=retDict['comment']
	command=retDict['command']

	result = retDict['retVal']
	dict['path']=path
	dict['baseOrig']=baseOrig
	dict['dirUpFull']=dirUpFull
	dict['dirUp']=dirUp
	dict['tempSplitFull']=tempSplitFull
	dict['comment']=comment
	dict['command']=command
	if result != 0:
		dict['retVal']=1
	else:	
		dict['retVal']=0
	return(dict)
	
def tarPyFunc ( src, dest, TEMP ):
	dict = {'function' : 'dittoFunc'}
	startTime = datetime.datetime.now()
	curDir=os.getcwd()
	srcBase=os.path.basename(src)
	srcDirName=os.path.dirname(src)
	os.chdir(srcDirName)
	
	tar = tarfile.open(dest, "w")
	tar.add(srcBase)
	tar.close()
	endTime = datetime.datetime.now()
	dict['command'] = "tar.add(srcBase)"
	if os.path.exists(dest):
		timeDict = timeFunc.timeDuration2 (endTime, startTime)
		dict['runTotalSeconds'] = timeDict['seconds']
		dict['runHours'] = timeDict['printHours']
		dict['runMins'] = timeDict['printMins']	
		dict['retVal'] = 0
		dict['error']= ""
	else:
		dict['retVal'] = 1
		dict['error']= "tar file was not created:  " + dest	
	os.chdir(curDir)
	return(dict)
	
def dittoFunc ( src, dest, TEMP ):
	dict = {'function' : 'dittoFunc'}
	startTime = datetime.datetime.now()
	curDir=os.getcwd()
	srcBase=os.path.basename(src)
	srcDirName=os.path.dirname(src)
	destBase=os.path.basename(dest)
	destDirName=os.path.dirname(dest) +"/"
	os.chdir(srcDirName)
	dittoErrorFile = TEMP + "dittoError.txt"
	dittoOutputFile = TEMP + "dittoOutput.txt"
	command = "/usr/bin/ditto -V --rsrc -c -z " + srcBase + " " + dest + " 2> " + dittoErrorFile + "  > " + dittoOutputFile 
	dict['command']= command
	dict['command']= command
	result=comWrap.comWrap (command)
	f = open(dittoOutputFile, 'r')
	output = f.read()
	f.close
	dict['output'] = output
	if os.path.exists(dest):
		endTime = datetime.datetime.now()
		timeDict = timeFunc.timeDuration2 (endTime, startTime)
		dict['runTotalSeconds'] = timeDict['seconds']
		dict['retVal'] = 0
		dict['error']= ""
	else:
		dict['retVal'] = 1
		f = open(dittoErrorFile, 'r')
		error = f.read()
		f.close
		dict['error']= error
	os.chdir(curDir)
	return(dict)
			  
def splitArchive ( Amount, pathArchive, pathSplit ):
	#split -a 3 -b $splitAmount ${tempTar}$tarFile "${tempSplit}$tarFile.part-"
	command = "/usr/bin/split -a 3 -b " + Amount + " " + pathArchive + " " + pathSplit
	result=comWrap.comWrap (command)
	return(result)

def splitArchiveReturn ( Amount, pathArchive, pathSplit ):
	dict = {'function' : 'splitArchiveReturn'}
	dict['retVal']=0
	dict['error']=""
	dict['comment']=""
	#split -a 3 -b $splitAmount ${tempTar}$tarFile "${tempSplit}$tarFile.part-"
	command = "/usr/bin/split -a 3 -b " + Amount + " " + pathArchive + " " + pathSplit
	result=comWrap.comWrap (command)
	dict['command']=command
	dict['result']=result
	return dict
	
def tarFunc2 ( pathArchive, localDir, tarErrorFile ):
	dict = {'function' : 'tarFunc2'}
	startTime = datetime.datetime.now()
	curDir=os.getcwd()
	#gnutar -cvf  $tempTar$tarFile "$local_dir"
	base=os.path.basename(localDir)
	dirName=os.path.dirname(localDir)
	os.chdir(dirName)
	command = "/usr/bin/tar -cf " + pathArchive + " " + base + " 2> " + tarErrorFile
	dict['command']= command
	result=comWrap.comWrap (command)
	if os.path.exists(pathArchive):
		endTime = datetime.datetime.now()
		timeDict = timeFunc.timeDuration2 (endTime, startTime)
		dict['runTotalSeconds'] = timeDict['seconds']
		dict['retVal'] = 0
		dict['tarErrorFile']= ""
	else:
		dict['retVal'] = 1
		f = open(tarErrorFile, 'r')
		output = f.read()
		f.close
		dict['tarErrorFile']= output
	os.chdir(curDir)
	return(dict)
		
def tarFunc ( pathArchive, localDir ):
	#gnutar -cvf  $tempTar$tarFile "$local_dir"
	command = "/usr/bin/gnutar -cf " + pathArchive + " " + localDir
	result=comWrap.comWrap (command)
	return(result)
	
def tarFuncReturn ( pathArchive, localDir ):
	#gnutar -cvf  $tempTar$tarFile "$local_dir"
	dict = {'function' : 'tarFuncReturn'}
	dict['retVal']=0
	dict['error']=""
	dict['comment']=""
	command = "/usr/bin/gnutar -cf " + pathArchive + " " + localDir
	dict['command']=command
	result=comWrap.comWrap (command)
	dict['result']=str(result)
	return dict
