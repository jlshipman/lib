#!/usr/bin/python

import os.path
import sys
import os
import glob
import pwd
import grp
import re
import inspect
import tarfile
sys.path.append('lib')
import comWrap
import math
import datetime
from time import *
from log import *
from simpleMail import *
from listFunctions import *
from archiveFunc import *
import hashlib
import shutil
import fcntl
import hashlib
import funcReturn

fileHandle = None

#find and remove string in file
def findRemoveString(string, filePath):
	retObj = funcReturn.funcReturn('findRemoveString')
#	print "filePath:  " + filePath
#	print "string:  " + string
	
	cwd = os.getcwd()
#	print "cwd:  " + cwd

	dir = os.path.dirname(filePath)
#	print "dir:  " + dir

	base = os.path.basename(filePath)
#	print "base:  " + base

	os.chdir(dir)
	cwd = os.getcwd()
#	print "cwd:  " + cwd

	try:
		f = open(base,"r")
	except Exception as e:
		retObj.setError("open " + base + " for read "  + str(e))
#		print "open " + base + " for read "  +  str(e)	
		return retObj

	try:
		lines = f.read().splitlines()
	except Exception as e:
		retObj.setError("read error: "  + str(e))
#		print "read error: "  + str(e)
		return retObj
	f.close()	

#	for line in lines:
#		print "line:  " + line
	if string in lines:
#		print "string in list"
		try:
			f = open(base,"w")
		except Exception as e:
			retObj.setError("open " + base + " for write "  + e)
#			print "open " + base + " for write "  + e
			return retObj
	
		for line in lines:
			if line!=string:
				f.write(line+"\n")
		retObj.setRetVal(0)
   	else:
#   		print "string NOT in list"
   		retObj.setError(string + " not found in "  + filePath)
	f.close()	
			
	return retObj
	
#find string in file
def findString(string, filePath):
	retObj = funcReturn.funcReturn('findString')
	if string in open(filePath).read():
		retObj.setRetVal(0)
	return retObj	

#get File Stats based on a string input with file name with spaces
def fileStatsNoGroupsSpacesFromString(theString):
	retObj = funcReturn.funcReturn('fileStatsFromString')
	foundList = listFunctions.stringToList(theString)
	sizeList = len(foundList)
	#print "\tsizeList" + " : " + str(sizeList)
	fileName = ""
	if sizeList > 8: 
		resultDict = {}
		resultDict['posix']=foundList[0]
		resultDict['links']=foundList[1]
		resultDict['owner']=foundList[2]
		resultDict['size']=foundList[3]
		resultDict['modified']=foundList[4] + " " + foundList[5] + " " + foundList[6]
		for n in range(7, sizeList):
			if n == sizeList -1:
				fileName = fileName + foundList[n]
			else:
				fileName = fileName + foundList[n] + " "
		resultDict['filename']=fileName
# 		for keys,values in resultDict.items():
# 			print "\t" + keys + " : " + values
		retObj.setRetVal(0)
		retObj.setResult(resultDict)
	return retObj	
	
	
#get File Stats based on a string input
def fileStatsNoGroupsFromString(theString):
	retObj = funcReturn.funcReturn('fileStatsFromString')
	foundList = listFunctions.stringToList(theString)
	sizeList = len(foundList)
	#print "\tsizeList" + " : " + str(sizeList)

	if sizeList == 8: 
		resultDict = {}
		resultDict['posix']=foundList[0]
		resultDict['links']=foundList[1]
		resultDict['owner']=foundList[2]
		resultDict['size']=foundList[3]
		resultDict['modified']=foundList[4] + " " + foundList[5] + " " + foundList[6]
		resultDict['filename']=foundList[7].strip()
# 		for keys,values in resultDict.items():
# 			print "\t" + keys + " : " + values
		retObj.setRetVal(0)
		retObj.setResult(resultDict)
	return retObj	
	
#get File Stats based on a string input
def fileStatsFromString(theString):
	retObj = funcReturn.funcReturn('fileStatsFromString')
	foundList = listFunctions.stringToList(theString)
	sizeList = len(foundList)
	#print "\tsizeList" + " : " + str(sizeList)

	if sizeList == 9: 
		resultDict = {}
		resultDict['posix']=foundList[0]
		resultDict['links']=foundList[1]
		resultDict['owner']=foundList[2]
		resultDict['groups']=foundList[3]
		resultDict['size']=foundList[4]
		resultDict['modified']=foundList[5] + " " + foundList[6] + " " + foundList[7]
		resultDict['filename']=foundList[8].strip()
# 		for keys,values in resultDict.items():
# 			print "\t" + keys + " : " + values
		retObj.setRetVal(0)
		retObj.setResult(resultDict)
		
	if sizeList > 9:
		resultDict = {}
		resultDict['posix']=foundList[0]
		resultDict['links']=foundList[1]
		resultDict['owner']=foundList[2]
		resultDict['groups']=foundList[3]
		resultDict['size']=foundList[4]
		resultDict['modified']=foundList[5] + " " + foundList[6] + " " + foundList[7]
		filename = ""
		for i in range(8, sizeList):
			filename = foundList[i] + " " 
		resultDict['filename']=filename.strip()
# 		for keys,values in resultDict.items():
# 			print "\t" + keys + " : " + values
		retObj.setRetVal(0)
		retObj.setResult(resultDict)
	return retObj	
	
#delete files with given suffix
def deleteFiles(dirPath, suffix):
	dict = {'function' : 'deleteFiles'}
	dict['retVal']=0
	dict['error']=""
	dict['comment']=""
	if fileExist(dirPath):		
		for the_file in os.listdir(dirPath):
			file_path = os.path.join(dirPath, the_file)
			try:
				if os.path.isfile(file_path) and the_file.endswith(suffix):
					os.unlink(file_path)
			except Exception, e:
				dict['error']="exception on deleting file: " + the_file + "  " + e + "\n"
				dict['retVal']=1
				return dict
	else:
		dict['error']="directory path did not exist:  " + dirPath + "\n"
		dict['retVal']=1
	return dict
	
#create a number of files with given suffix
def createFiles(dirPath, amount, base, suffix):
	dict = {'function' : 'createFiles'}
	dict['retVal']=0
	dict['error']=""
	dict['comment']=""
	if fileExist(dirPath):		
		for x in range(0, amount):
			filePath = dirPath + "/" + base + str(x) + suffix
			fileCreate( filePath )
	else:
		dict['error']="directory path did not exist:  " + dirPath + "\n"
		dict['retVal']=1
	return dict

#print out file contents
def printFile (path):
	inFile = open(path, 'r')
	contents = inFile.read()
	inFile.close()
	print(contents)

def printFilePrepend (path, prefix):
	inFile = open(path, 'r')
	for line in inFile.readlines():
		print prefix, line.rstrip("\n")
	inFile.close()
	
#change the flages to nouchg 
def nouchgDict ( fileDir ):
	dict = {'function' : 'nouchgDict'}
	command = "/usr/bin/chflags -R nouchg " + fileDir
	dict['command']= command
	retVal = comWrap.comWrap (command)
	dict['retVal']= retVal
	return dict
	
#change the flages to nouchg 
def nouchg ( fileDir ):
	command = "/usr/bin/chflags -R nouchg " + fileDir
	retVal = comWrap.comWrap (command)
	return retVal
	
def countLinesInFile ( file ):
	non_blank_count = 0

	with open(file) as infp:
		for line in infp:
			if line.strip():
			  non_blank_count += 1
	return non_blank_count
	
def normalizeNewLinesFile(inputFile, outputFile):
	f= open(inputFile, 'r')
	lines = f.readlines()
	f.close()
	
	if fileExist (outputFile):
		fileDelete(outputFile)
	f=open(outputFile, 'w')
	
	for line in lines:
		modLine = line.replace('\r\n', '\n').replace('\r', '\n')
		f.write(modLine)
	f.close()

def fileIsLocked(filePath):
    global file_handle 
    fileHandle= open(filePath, 'w')
    try:
        fcntl.lockf(fileHandle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return False
    except IOError:
        return True

def copyFileRetObj (src, dst):
	retObj = funcReturn.funcReturn('copyfile')
	src = src.strip()
	dst = dst.strip()	
	if fileExist ( dst ):
		os.unlink(dst)	
	
	dstDir = os.path.dirname(dst)	
	
	try:
		shutil.copyfile(src, dst)
		retVal= 0
		error= "none"
	except Exception as e:
		error= "unknown"
		if not isFile(src):
			error= "souce file, " +src + ", is not a file"
		elif fileExist (src):
			error= "souce file, " +src + ", does not exist"
		elif not isinstance( src, str ):
			error= "souce file, " +src + ", is not a string"		
		elif len(src) < 1:
			error= "souce file, " +src + ", is of length less than 1"
		elif not fileExist (dstDir):
			error= "destination directory does not exist"
		else:
			error= "unknown"
			retObj.setError(error)
		retVal= 1
	
	retObj.setRetVal(retVal)
	
	return retObj
	       
def copyFile (src, dst):
	dict = {'function' : 'copyfile'}
	dict['command']= ""
	src = src.strip()
	dst = dst.strip()	
	if fileExist ( dst ):
		os.unlink(dst)	
	
	dstDir = os.path.dirname(dst)	
	
	try:
		shutil.copyfile(src, dst)
		dict['retVal']= 0
		dict['error']= "none"
	except Exception as e:
		dict['error']= "unknown"
		if not isFile(src):
			dict['error']= "souce file, " +src + ", is not a file"
		elif fileExist (src):
			dict['error']= "souce file, " +src + ", does not exist"
		elif not isinstance( src, str ):
			dict['error']= "souce file, " +src + ", is not a string"		
		elif len(src) < 1:
			dict['error']= "souce file, " +src + ", is of length less than 1"
		elif not fileExist (dstDir):
			dict['error']= "destination directory does not exist"
		else:
			dict['error']= "unknown"
			
		dict['retVal']= 1
	return dict
	
def moveFileRetObj (src, dst):
	retObj = funcReturn.funcReturn('moveFileRetObj')
	src = src.strip()
	dst = dst.strip()	
	if fileExist ( dst ):
		os.unlink(dst)	
	
	dstDir = os.path.dirname(dst)	
	
	try:
		shutil.movefile(src, dst)
		retVal= 0
		error= "none"
	except Exception as e:
		error= "unknown"
		if not isFile(src):
			error= "souce file, " +src + ", is not a file"
		elif not fileExist (src):
			error= "souce file, " +src + ", does not exist"
		elif not isinstance( src, str ):
			error= "souce file, " +src + ", is not a string"		
		elif len(src) < 1:
			error= "souce file, " +src + ", is of length less than 1"
		elif not fileExist (dstDir):
			error= "destination directory does not exist"
		else:
			error= "unknown"
		retObj.setError(error)
		retVal= 1
	
	retObj.setRetVal(retVal)
	
	return retObj
		
def fileMove2 (src, dst):
	dict = {'function' : 'fileMove2'}
	dict['command']= ""
	src = src.strip()
	dst = dst.strip()	
	if fileExist ( dst ):
		os.unlink(dst)	
	
	dstDir = os.path.dirname(dst)	
	
	try:
		shutil.move(src, dst)
		dict['retVal']= 0
		dict['error']= "none"
	except Exception as e:
		dict['error']= "unknown"
		if not isFile(src):
			dict['error']= "souce file, " +src + ", is not a file"		
		elif not isinstance( src, str ):
			dict['error']= "souce file, " +src + ", is not a string"		
		elif len(src) < 1:
			dict['error']= "souce file, " +src + ", is of length less than 1"
		elif not fileExist (dstDir):
			dict['error']= "destination directory does not exist"
		else:
			dict['error']= "unknown"
			
		dict['retVal']= 1
	return dict
		       
def fileMove (src, dst):
	dict = {'function' : 'fileMove'}
	dict['command']= ""
	
	if not isFile(src):
		dict['retVal']= 1
		dict['error']= "souce file, " +src + ", is not a file"
		return dict
	
	if not isinstance( src, str ):
		dict['retVal']= 1
		dict['error']= "souce file, " +src + ", is not a string"
		return dict
		
	if len(src) < 1:
		dict['retVal']= 1
		dict['error']= "souce file, " +src + ", is of length less than 1"
		return dict
		
	if fileExist ( dst ):
		os.unlink(dst)
	resultDict = comWrap.comWrapMv(src, dst)
	result = resultDict['retVal']
	command = resultDict['command']
	dict['command']= command
	if result == 0:
		dict['retVal']= 0
		dict['error']= "none"
		return dict
	else:
		dict['retVal']= 1
		dict['error']= resultDict['error']
		return dict


def fileMoveObj (src, dst):
	retObj = funcReturn.funcReturn('fileMoveObj')
	
	if not isFile(src):
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is not a file"
		retObj.setError(error)
		return retObj
	
	if not isinstance( src, str ):
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is not a string"
		retObj.setError(error)
		return retObj
		
	if len(src) < 1:
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is of length less than 1"
		retObj.setError(error)
		return retObj
		
	if fileExist ( dst ):
		os.unlink(dst)
	resultDict = comWrap.comWrapMv(src, dst)
	result = resultDict['retVal']
	command = resultDict['command']
	retObj.setCommand(command)
	if result == 0:
		retObj.setRetVal(0)
		return retObj
	else:
		retObj.setRetVal(1)
		error = resultDict['error']
		retObj.setError(error)
		return retObj

def fileMoveSudoObj (src, dst):
	retObj = funcReturn.funcReturn('fileMoveObj')
	
	if not isFile(src):
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is not a file"
		retObj.setError(error)
		return retObj
	
	if not isinstance( src, str ):
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is not a string"
		retObj.setError(error)
		return retObj
		
	if len(src) < 1:
		retObj.setRetVal(1)
		error = "souce file, " +src + ", is of length less than 1"
		retObj.setError(error)
		return retObj
		
	if fileExist ( dst ):
		os.unlink(dst)
	retObjMb = comWrap.comWrapMvSudo(src, dst)
	result = retObjMb.getRetVal()
	command = retObjMb.getCommand()
	retObj.setCommand(command)
	if result == 0:
		retObj.setRetVal(0)
		return retObj
	else:
		retObj.setRetVal(1)
		error = resultDict['error']
		retObj.setError(error)
		return retObj		


def checkSum (file):
	return hashlib.md5(file).hexdigest()			

def checkSum2 ( fileCheckSum, ouptutFile ):
	dict = {'function' : 'checkSum2'}
	command = "/usr/bin/sum " + fileCheckSum 
	dict['command']= command
	result= comWrap.comWrap (command)
	theString=listToString(result)
	if fileExist ( ouptutFile ):
		os.unlink(ouptutFile)
	fileCreate( ouptutFile )
	writeToFile (theString, ouptutFile)
	dict['result']= theString
	dict['retVal']=0
	return(dict)

def checkSum3 ( fileToCheckSum, ouptutFile ):
	dict = {'function' : 'checkSum3'}
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	dict['error']= "none"
	dict['retVal']=0
	try:
		f = open(fileToCheckSum, 'rb')
	except Exception:
		dict['error']= "unable to open fileToCheckSum:  " + fileToCheckSum
		dict['retVal']=1
		return(dict)
		
	try:	
		buf = f.read(BLOCKSIZE)
		while len(buf) > 0:
			hasher.update(buf)
			buf = f.read(BLOCKSIZE)
		f.close()
	except Exception as e:
		dict['error']= "unable to create checksum"
		dict['retVal']=1
		return(dict)
		
	if fileExist ( ouptutFile ):
		os.unlink(ouptutFile)
	fileCreate( ouptutFile )
	writeToFile (hasher.hexdigest(), ouptutFile)
	return(dict)
	
def checkSumObj ( fileToCheckSum ):
	print "checkSumObj"
	print "\tfileToCheckSum:  " + fileToCheckSum
	retObj = funcReturn.funcReturn('checkSumObj')
	base = os.path.basename(fileToCheckSum)
	dir =  os.path.dirname(fileToCheckSum)
	curDir=os.getcwd()
	output = "curDir:  " + curDir + "\n"
	print "\tcurDir:  " + curDir
	os.chdir(dir)
	newDir=os.getcwd()
	output += "newDir:  " + newDir + "\n"
	print "\tnewDir:  " + newDir
	#command = ["/usr/bin/sum", base]
	#retObjBash = comWrap.comWrapRetObj(command)
	#output += listFunctions.listToString(command)

	command = "/usr/bin/sum " + base
	output += command
	retObjBash = comWrap.comWrapString(command)
	retObj.setCommand(command)
	stdOut = retObjBash.getStdout().strip()
	bashRetVal = retObjBash.getRetVal()
	print "\tcommand:  " + str(command)
	print "\tbashRetVal:  " + str(bashRetVal)
	os.chdir(curDir)
	if bashRetVal == 0:
		print "\tsetRetVal 0"
		retObj.setRetVal(0)
	else:
		print "\tsetRetVal 1"
		retObj.setRetVal(1)
	print "\tstdOut:  " + str(stdOut)	
	retObj.setStdout(stdOut)
	retObj.setComment(output)
	return retObj
	
def convertNameToCamel ( nameString, findChar):
	resultList=findOccuranceIndexes ( nameString, findChar)
	nextChar = []
	for r in resultList:
		n = r + 1
		pattern = re.compile(r'[a-zA-Z]')
		if pattern.findall(nameString[n]):
			stringList = list(nameString)
			stringList[n]=nameString[n].upper()
			nameString="".join(stringList)
	nameList=nameString.split("_")
	listSize=len(nameList)	
	newList = []
	for idx, val in enumerate(nameList):
		if idx == 0:
			newList.append(val)
		else:
			reg=re.compile('[a-zA-Z]+')
			test1=reg.match(nameList[idx-1])
			test2=reg.match(nameList[idx])
			if test1 and test2:
				newList.append(val)
			else:
				newList.append("_"+val)
	newName="".join(newList)
	return newName
	
def findOccuranceIndexes ( nameString, findChar):
	resultList=[m.start() for m in re.finditer(findChar, nameString)]
	return resultList

def removeBadChar2 ( nameString ):
	#nameString=nameString.replace(" ","")
	nameString=nameString.replace("-","_")
	nameString=nameString.replace("*","")
	nameString=nameString.replace("|","_")
	nameString=nameString.replace("'","")
	nameString=nameString.replace("&","")
	nameString=nameString.replace("'","")
	
	# Remove all non-word characters (everything except numbers and letters)
	nameString = re.sub('\s+', '', nameString)   

	return nameString	

def removeBadChar ( nameString ):
	#nameString=nameString.replace(" ","")
	nameString=nameString.replace("-","_")
	nameString=nameString.replace("*","")
	nameString=nameString.replace("|","_")
	nameString=nameString.replace("'","")
	nameString=nameString.replace("&","")
	nameString=nameString.replace("'","")
	
	# Remove all non-word characters (everything except numbers and letters)
	nameString = re.sub('\s+', '', nameString)

	# remove all [^A-Za-z0-9_]
	nameString = re.sub('\W', '', nameString)    

	return nameString

#expects number and file units	
def convertToBytes(size, unit):
	units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	chunk = 1024
	exponent = units.index(unit)
	result = size*chunk**exponent
	return result

#expects number and units	
def convertToBytes2(size, unit):
	retObj = funcReturn.funcReturn('convertToBytes2')
	units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	chunk = 1024
	exponent = units.index(unit)
	result = size*chunk**exponent
	retObj.setComment("size: " + str(size) +  "   unit:  " + unit)
	retObj.setResult(result)
	return retObj
	
#expects number and file units
def convertToMB(size, unit):
	units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
	chunk = 1024
	exponent = units.index(unit)
	result = size*chunk**exponent
	return result
		
#return file size in bytes
def fileSize (file):
	if os.path.exists(file):
		size=os.path.getsize(file)
	else:
		size=-1
	return size

#read first line of a file	
def readFirstLineFile(file):
	f = open(file, 'r')
	firstLine = f.readline().strip()
	f.close()
	return firstLine
	
#create a new file from list	
def writeToFile( item, file):
	#print item
	#print file
	f = open(file, 'w+')
	f.write("%s" % item)
	f.close()
	
#create a new file from list pf lists	
def listofListToFile( list, file, sep):
	#print "file:  "  + file
	if os.path.exists(file):
		os.unlink(file)
	f = open(file, 'w+')
	for item in list:
		string=sep.join(item)
		f.write("%s\n" % string)
	f.close()
			
#create a new file from list	
def listToFile( list, file):
	#print "file:  "  + file
	if os.path.exists(file):
		os.unlink(file)
	f = open(file, 'w+')
	for item in list:
		f.write("%s\n" % item)
	f.close()
	
#Returns the current line number in our program.
def lineNo():
    return inspect.currentframe().f_back.f_lineno
    
def fileCreate ( filePath ):
	file = open(filePath, 'w')
	file.write('')
	file.close()

def fileCreateWrite ( filePath, text):
	print "fileCreateWrite"
	print "\tfilePath:  " + filePath
	print "\ttext:  " + text
	retObj = funcReturn.funcReturn('fileCreateWrite')
	
	if fileExist(filePath):
		fileDelete(filePath)
		print "f\tile deleted"
	
	command = "echo "  + '"' + text + '" > ' + filePath
	print "\tcommand:  " + command
	retObjBash = comWrap.comWrapString(command)
	bashRetVal = retObjBash.getRetVal()
	if bashRetVal == 0:
		print "\tsetRetVal 0"
		retObj.setRetVal(0)
	else:
		print "\tsetRetVal 1"
		retObj.setRetVal(1)

	return retObj
	
def isFile ( path ):
	return os.path.isfile(path)
	
def fileExist ( filePath ):
	return os.path.exists(filePath)

def fileDirDeleteSudo ( filePath ):
	retObj=funcReturn.funcReturn('fileDirDelete')
	appleCommand = ["sudo", "/bin/rm", "-rf", filePath]
	retObjRM = comWrap.comWrapRetObj(appleCommand)
	retVal=retObjRM.getRetVal()	
	output = listFunctions.listToString(appleCommand)
	retObj.setComment(output)
	if not (os.path.exists ( filePath )):
		retObj.setRetVal(0)
		retObj.setStderr(retObjRM.getStderr() + retObjRM.getStdout())
	else:
		retObj.setRetVal(1)
	return retObj	

def fileDirDelete ( filePath ):
	retObj=funcReturn.funcReturn('fileDirDelete')
	appleCommand = ["/bin/rm", "-rf", filePath]
	retObjRM = comWrap.comWrapRetObj(appleCommand)
	retVal=retObjRM.getRetVal()	
	output = listFunctions.listToString(appleCommand)
	retObj.setComment(output)
	if not (os.path.exists ( filePath )):
		retObj.setRetVal(0)
		retObj.setStderr(retObjRM.getStderr() + retObjRM.getStdout())
	else:
		retObj.setRetVal(1)
	return retObj	
	
def fileDirDeleteBash ( filePath ):
	dict = {'function' : 'fileDirDeleteBash'}
	dict['filePath'] = filePath
	comWrapCommand = '/bin/rm -rf ' + filePath
	dict['command'] = comWrapCommand
	command = comWrap.WrapCommand (comWrapCommand)
	result = command ()
	if not (os.path.exists ( filePath )):
		dict['retVal'] = 0
	else:
		dict['retVal'] = 1
	return dict	
		
def fileDelete (filePath):
	try:
		os.unlink(filePath)
	except Exception:
		print os.getcwd()
		print filePath

def fileDeleteVerbose (filePath):
	dict = {'function' : 'fileDeleteVerbose'}
	dict['filePath'] = filePath
	try:
		os.unlink(filePath)
	except Exception as e:
		dict['error'] = e
		
	if not (os.path.exists ( filePath )):
		dict['retVal'] = 0
	else:
		dict['retVal'] = 1
	return dict	
				
def fileDeleteReturn ( filePath ):
	try:
		os.unlink(filePath)
	except Exception:
		print os.getcwd()
		print filePath
		
	if not (os.path.exists ( filePath )):
		return(0)
	else:
		return(1)

#delete files and directories matching giving pattern within a 
#starting top directory
def purge(dir, pattern, inclusive=True):
    regexObj = re.compile(pattern)
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            path = os.path.join(root, name)
            if bool(regexObj.search(path)) == bool(inclusive):
                os.remove(path)
        for name in dirs:
            path = os.path.join(root, name)
            if len(os.listdir(path)) == 0:
                os.rmdir(path)
    		
def makeArchive ( archiveNameFull, locationPathFull):
	curDir = os.getcwd()
	dir = os.path.dirname(locationPathFull)
	base = os.path.basename(locationPathFull)
	os.chdir(dir)
	tar = tarfile.open(archiveNameFull, "a")
	tar.add(base)
	os.chdir(curDir)

def sendCSS ( paraList ):
	dt1=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
	file =  paraList [0]
	cssPath =  paraList [1]
	errorFile =  paraList [2]
	resultDict=comWrap.comWrapMasput ( file, cssPath , errorFile )
	result = resultDict[ 'retVal']
	size=fileSize(file)
	dt2=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
 	date1 = datetime.datetime.strptime(dt1, "%Y-%b-%d-%H:%M:%S") 
 	date2 = datetime.datetime.strptime(dt2, "%Y-%b-%d-%H:%M:%S")
	tdelta=(date2 - date1)
 	delta_seconds = (tdelta.days * 60 * 60 * 24) + tdelta.seconds + ((tdelta.microseconds + 500000) / 1000000) 
 	seconds = delta_seconds
 	paraList.append (result)
 	paraList.append (size) 
 	paraList.append (seconds) 
 	return resultDict
 
def makeArchiveSplitReturn (paraList):
	dict = {'function' : 'makeArchiveSplitReturn'}
	dict['retVal']=0
	dict['error']=""
	dict['comment']=""

	dt1=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
	archiveNameFull =  paraList [0]
	locationPathFull =  paraList [1]
	splitFull =  paraList [2]
	Amount =  paraList [3]
	
	dict['dt1']=dt1
	dict['archiveNameFull']=archiveNameFull
	dict['locationPathFull']=locationPathFull
	dict['splitFull']=splitFull
	dict['Amount']=Amount
	
	curDir = os.getcwd()
	dir = os.path.dirname(locationPathFull)
	base = os.path.basename(locationPathFull)
	os.chdir(dir)
	
	resultDict = tarFuncReturn (archiveNameFull, base)
	size=fileSize(archiveNameFull)
	os.chdir(curDir)
	
 	resultDict = splitArchiveReturn (Amount, archiveNameFull, splitFull)
 	dt2=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
 	date1 = datetime.datetime.strptime(dt1, "%Y-%b-%d-%H:%M:%S") 
 	date2 = datetime.datetime.strptime(dt2, "%Y-%b-%d-%H:%M:%S") 
   	tdelta=(date2 - date1)
 	delta_seconds = (tdelta.days * 60 * 60 * 24) + tdelta.seconds + ((tdelta.microseconds + 500000) / 1000000) 
 	seconds = delta_seconds
 	
  	if resultDict['result'] == 0:
  		if (os.path.exists ( archiveNameFull )): 
 			os.remove(archiveNameFull)
	dict['size']=size
	dict['seconds']=seconds 	

	return dict
 	
def makeArchiveSplit (paraList):
	dt1=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
	archiveNameFull =  paraList [0]
	locationPathFull =  paraList [1]
	splitFull =  paraList [2]
	Amount =  paraList [3]
	curDir = os.getcwd()
	dir = os.path.dirname(locationPathFull)
	base = os.path.basename(locationPathFull)
	os.chdir(dir)
	result = tarFunc (archiveNameFull, base)
	size=fileSize(archiveNameFull)
	os.chdir(curDir)
 	result = splitArchive (Amount, archiveNameFull, splitFull)
 	dt2=datetime.datetime.now().strftime("%Y-%b-%d-%H:%M:%S") 
 	date1 = datetime.datetime.strptime(dt1, "%Y-%b-%d-%H:%M:%S") 
 	date2 = datetime.datetime.strptime(dt2, "%Y-%b-%d-%H:%M:%S") 
   	tdelta=(date2 - date1)
 	delta_seconds = (tdelta.days * 60 * 60 * 24) + tdelta.seconds + ((tdelta.microseconds + 500000) / 1000000) 
 	seconds = delta_seconds
  	if result == 0:
  		if (os.path.exists ( archiveNameFull )): 
 			os.remove(archiveNameFull)
 	paraList.append (size) 
 	paraList.append (seconds) 
		
def isSticky(path):
    return os.stat(path).st_mode & 01000 == 01000
