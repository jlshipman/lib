#!/usr/bin/python
# try:
import pwd
import sys
import os
import glob
import shutil 
import errno
import pwd
import grp
import re
import datetime
import comWrap
import listFunctions
from os.path import join, getsize
sys.path.append('lib')
from fileFunctions import *
from timeFunc import *
import funcReturn
import fileFunctions


#set owner and posix recursively
#does not set the top of tree
def setPosix ( path, own, group, priv ):
	retObj=funcReturn.funcReturn('setPosix')
	path = path.strip()
	own = own.strip()
	group = group.strip()
	
	ownID = pwd.getpwnam(own).pw_uid
	groupID = grp.getgrnam(group).gr_gid
	for root, dirs, files in os.walk(path): 
	  for d in dirs:  
		dirPath = os.path.join(root, d)
		if os.path.exists(dirPath):
			try:
				os.chmod(dirPath, priv)
			except:
				error =  "  unable to chmod " + d + " to privilege " + str(priv)
				#print error	
				retObj.setError(error)
				return retObj
				
			try:
				os.chown(dirPath, ownID, groupID)
			except:
				error =  "unable to chown " + d + " to owner " +  str(ownID)
	 			#print error	
				retObj.setError(error)
				return retObj
				
	  for f in files:
		filePath = os.path.join(root, f)
		if os.path.exists(filePath):
			try:
				os.chmod(filePath, priv)
			except:
				error =  "unable to chmod file " + f + " to privilege " + str(priv)
				# error	
				retObj.setError(error)
				return retObj
			try:
				os.chown(filePath, ownID, groupID)
			except:
				error = "unable to chown file " + f + " to owner " + str(ownID)
				#print error	
				retObj.setError(error)
				return retObj	
				
	retObj.setRetVal(0)
	return retObj				
# 	
# except ImportError:
# 	print "missing modules for directory.py"
# 	sys.exit(1)
#move contents from one directory to another expects contents to be a file
def moveDirContents(srcDir, dstDir):
	retObj=funcReturn.funcReturn('moveDirContents')
	moveList = []
	for the_file in os.listdir(srcDir):
		srcFilePath = os.path.join(srcDir, the_file)
		dstFilePath = os.path.join(dstDir, the_file)	
		try:
			if os.path.isfile(srcFilePath):
				shutil.move(srcFilePath, dstFilePath)
				moveList.append(srcFilePath)
			#elif os.path.isdir(filePath): shutil.rmtree(filePath)
		except Exception as e:
			error = "problem moving:  " + srcFilePath + "  error:  " + E
			#print(e)	
			retObj.setError(error)
			retObj.setResult(moveList)
			return retObj	
	retObj.setRetVal(0)
	retObj.setResult(moveList)
	return retObj


#delete contents of directory expects contents to be a file
def deleteDirContents(dirPath):
	retObj=funcReturn.funcReturn('deleteDirContents')
	deleteList = []
	for the_file in os.listdir(dirPath):
		filePath = os.path.join(dirPath, the_file)
		try:
			if os.path.isfile(filePath):
				os.unlink(filePath)
				deleteList.append(filePath)
			#elif os.path.isdir(filePath): shutil.rmtree(filePath)
		except Exception as e:
			error = "problem deleting:  " + filePath + "  error:  " + E
			#print(e)	
			retObj.setError(error)
			retObj.setResult(deleteList)
			return retObj	
	retObj.setRetVal(0)
	retObj.setResult(deleteList)
	return retObj
	
#return list of files in dirPath with said suffix
def listFilesSuffixNoDups2 (
	dirPath, #directory to search
	suffix  #suffix with . to search for
	):
	resultList = []
	retObj=funcReturn.funcReturn('listFilesSuffixNoDups2')
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if file.endswith(suffix):
				if file not in resultList:
					resultList.append(os.path.join(root, file))
	retObj.setResult(resultList)
	retObj.setRetVal(0)
	return retObj

#return list of files in dirPath with said suffix sorted by creation date
def listFilesSuffixSortCreate (
	dirPath, #directory to search
	suffix  #suffix with . to search for
	):
	resultList = []
	retObj=funcReturn.funcReturn('listFilesSortCreate')
	for root, dirs, files in os.walk(dirPath):
		for d in dirs:
			checkDir = os.path.join(root, d)
			dirPlusPattern = checkDir + "/*." + suffix
			files = glob.glob(dirPlusPattern)
			resultList = resultList + files
	
	resultList.sort(key=os.path.getmtime)
	retObj.setResult(resultList)
	retObj.setRetVal(0)
	return retObj

def mvDirSudo(source, destination):
	retObj=funcReturn.funcReturn('mvDir')
	
	#rm -f destination_path && \
	#cp -pRP source_file destination && \
	#rm -rf source_file
	
	#does destination path exist
	if os.path.exists(destination):	
		#delete destination path
		retObjRM=fileFunctions.fileDirDeleteSudo(destination)
		retVal=retObjRM.getRetVal()	
		if retVal == 1:
			error=retObjRM.getError() + "\n"
			error ='was unable to delete destination location:  ' + destination
			retObj.setError(error )
			retObj.setComment(retObjRM.getComment() )
			retObj.setCommand(retObjRM.getCommand() )
			return retObj
# 		else:
# 			print "deleted directory"
# 			sys.exit(1)
		
	#make destination directory
	retObjMakeDir = makeDirectoryBashSudo(destination)
	#print "getComment:  " + retObjMakeDir.getComment()
	#print "getCommand:  " + retObjMakeDir.getCommand()
	retVal = retObjMakeDir.getRetVal()	
	if retVal == 1:
		retObj.setError('could not make destination location:  ' + destination)
		retObj.setComment(retObjMakeDir.getComment() )
		retObj.setCommand(retObjMakeDir.getCommand() )
		return retObj
		
	appleCommand = ["sudo", "cp", "-pRP", source, destination]
	retObjCP = comWrap.comWrapRetObj(appleCommand)
	retVal=retObjCP.getRetVal()	
	if retVal == 1:
		retObj.setError('copy failed to destination location:  ' + destination)
		retObj.setCommand(retObjCP.getCommand() )
		return retObj

	#delete source path
	retObjDest=fileFunctions.fileDirDelete(source)
	retVal=retObjDest.getRetVal()	
	if retVal == 1:
		retObj.setError('was unable to delete source location:  ' + source)
		retObj.setCommand(retObjDest.getCommand() )
		return retObj
	
	retObj.setRetVal(0)
	return retObj		

def mvDir(source, destination):
	retObj=funcReturn.funcReturn('mvDir')
	
	#rm -f destination_path && \
	#cp -pRP source_file destination && \
	#rm -rf source_file
		
	#delete destination path
	retObjRM=fileFunctions.fileDirDelete(destination)
	retVal=retObjRM.getRetVal()	
	if retVal == 1:
		error=retObjRM.getError() + "\n"
		error = error + 'was unable to delete destination location:  ' + destination
		retObj.setError(error )
		retObj.setComment(retObjRM.getComment() )
		return retObj
		
	#make destination directory
	retObjMakeDir=makeDirectoryBash2(destination)
	#print "getComment:  " + retObjMakeDir.getComment()
	#print "getCommand:  " + retObjMakeDir.getCommand()
	if retVal == 1:
		retObj.setError('copy failed to destination location:  ' + destination)
		retObj.setComment(retObjMakeDir.getComment() )
		retObj.setCommand(retObjMakeDir.getCommand() )
		return retObj
		
	appleCommand = ["cp", "-pRP", source, destination]
	retObjCP = comWrap.comWrapRetObj(appleCommand)
	retVal=retObjCP.getRetVal()	
	if retVal == 1:
		retObj.setError('copy failed to destination location:  ' + destination)
		return retObj

	#delete source path
	retObjDest=fileFunctions.fileDirDelete(source)
	retVal=retObjDest.getRetVal()	
	if retVal == 1:
		retObj.setError('was unable to delete source location:  ' + source)
		return retObj
	
	retObj.setRetVal(0)
	return retObj
	
#return list of files in dirPath with said suffix
def listFilesSuffixNoDups (
	dirPath, #directory to search
	suffix  #suffix with . to search for
	):
	dict = {'function' : 'listFilesSuffixNoDups'}
	dict['numberOfRows']= 0
	resultList = []
	resultListFullPath = []
	resultListBoth = []
	resultListMetaData = []
	dict['amount'] = 0
	amount = 0
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if file.endswith(suffix):
				if file not in resultList:
					resultListFullPath.append(os.path.join(root, file))
					resultList.append(file)
					resultListBoth.append([file, os.path.join(root, file)])
					size=os.path.getsize(os.path.join(root, file))
					modTime=os.path.getmtime(os.path.join(root, file))
					resultListMetaData.append([file, os.path.join(root, file), str(size), str(modTime)])
					amount = amount + 1
	dict['resultList']= resultList
	dict['resultListFullPath']= resultListFullPath
	dict['resultListBoth']= resultListBoth
	dict['resultListMetaData']= resultListMetaData
	dict['amount']= amount
	return dict
	
#return list of files in dirPath with said suffix
def listFilesSuffix (dirPath, suffix):
	#print "listFilesSuffix"
	#print dirPath
	dict = {'function' : 'listFilesSuffix'}
	dict['numberOfRows']= 0
	resultList = []
	dict['amount'] = 0
	amount = 0
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			#print file
			if file.endswith(suffix):
				 resultList.append(file)
				 amount = amount + 1
	dict['resultList']= resultList
	dict['amount']= amount
	return dict
	
#return list of files in dirPath with said prefix
def listFilesPrefix (dirPath, prefix):
	dict = {'function' : 'listFilesPrefix'}
	dict['numberOfRows']= 0
	resultList = []
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			if file.startswith(suffix):
				 resultList.append(file)
	dict['resultList']= resultList
	return dict
	
def findDirectory(rootFolder, findDir, depth=1):
	dict = {'function' : 'findDirectory'}
	rootFolder = rootFolder.rstrip(os.path.sep)
	numSep = rootFolder.count(os.path.sep)
	for root, dirs, files in os.walk(rootFolder):
		for d in dirs:
			numSepThis = root.count(os.path.sep)
			test =  numSep + depth
			if numSep + depth >= numSepThis:	
				if d == findDir:
					path = os.path.join(root,d)
					dict['retVal']= 0
					dict['path']= path
					dict['depth'] = numSepThis - numSep + 1
					return dict
		  	else:	
				retVal = 1
				dict['retVal']= 1
				dict['depth'] = -1
				return dict
                    
def dirSize(start_path = '.'):
    total_size = 0
    total_size= os.path.getsize(start_path)
    return total_size

def getDirSize(start_path = '.'):
	retObj = funcReturn.funcReturn('getDirSize')
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	retObj.setRetVal(0)
	retObj.setResult(total_size)
	return retObj

def copyRecursiveDate(dsrc, ddst, lastRun):
# 	print "copyRecursive"
# 	print "   dsrc", dsrc
# 	print "   ddst", ddst
	#make the initial destination directory
	if not os.path.exists(ddst):
		os.makedirs(ddst)
	for root, dirs, files in os.walk(dsrc):
		for d in dirs:  
			fromPath = os.path.join(root, d)
			#print "      dir ",fromPath
			if os.path.exists(fromPath):
				t = os.path.getmtime(fromPath)
				fileModTime=date.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
				lastRunTime = stringToTime(lastRun)
				if time1BiggerThantime2 ( fileModTime, lastRunTime ):			
					toPath = fromPath.replace(dsrc, ddst)
					#print "      toPath ",toPath
					if not os.path.exists(toPath):
						os.makedirs(toPath)
		for f in files:
			fromPath = os.path.join(root, f)
			#print "file ",fromPath
			if os.path.exists(fromPath):
				t = os.path.getmtime(fromPath)
				fileModTime=date.fromtimestamp(t).strftime('%Y-%m-%d %H:%M')
				lastRunTime = stringToTime(lastRun)
				if time1BiggerThantime2 ( fileModTime, lastRunTime ):	
					toPath = fromPath.replace(dsrc, ddst)
					if not os.path.exists(toPath):
						 shutil.copyfile(fromPath, toPath)
					    
def copyRecursive(dsrc, ddst):
# 	print "copyRecursive"
# 	print "   dsrc", dsrc
# 	print "   ddst", ddst
	#make the initial destination directory
	if not os.path.exists(ddst):
		os.makedirs(ddst)
	for root, dirs, files in os.walk(dsrc):
		for d in dirs:  
			fromPath = os.path.join(root, d)
			#print "      dir ",fromPath
			if os.path.exists(fromPath):
				toPath = fromPath.replace(dsrc, ddst)
				#print "      toPath ",toPath
				if not os.path.exists(toPath):
					os.makedirs(toPath)
		for f in files:
			fromPath = os.path.join(root, f)
			#print "file ",fromPath
			if os.path.exists(fromPath):
				toPath = fromPath.replace(dsrc, ddst)
				if not os.path.exists(toPath):
					 shutil.copyfile(fromPath, toPath)
    
def countFilesWithPrefix (path, prefix):
	makeDirectory(path)
	list_dir = []
	list_dir = os.listdir(path)
	count = 0
	for file in list_dir:
		if file.startswith(prefix): # eg: 'begin_'
			count += 1
	return count

def countFiles (path):
  list_dir = []
  list_dir = os.listdir(path)
  count = 0
  for file in list_dir:
       count += 1
  return count
  
def listFiles (path, prefix):
	input = path + "/" + prefix + "*"
	files=glob.glob(path + "/" + prefix + "*")
	return files

def setToUnLock(dirPath):
	#sudo chflags -R nouchg <path>
	retObj = funcReturn.funcReturn('setToUnLock')
	dirPath = dirPath.strip()
	appleCommand = ["chflags", "-R", "nouchg", dirPath]
	output = listFunctions.listToString(appleCommand)	
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setComment(output)
	return retObj

def setGroupOwner(dirPath, own, group):
	#sudo chown -R ladmin:VideoEditors <path>
	retObj = funcReturn.funcReturn('setGroupOwner')
	dirPath = dirPath.strip()
	og = own + ":" + group
	appleCommand  = ["chown", "-R", og, dirPath]
	command = "chown -R " + og + " " + dirPath
	retObj.setCommand(command)
	output = listFunctions.listToString(appleCommand)	
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setComment(output)
	return retObj	

def setGroupOwnerSudo(dirPath, own, group):
	#sudo chown -R ladmin:VideoEditors <path>
	retObj = funcReturn.funcReturn('setGroupOwner')
	dirPath = dirPath.strip()
	og = own + ":" + group
	appleCommand  = ["sudo", "chown", "-R", og, dirPath]
	command = "sudo chown -R " + og + " " + dirPath
	retObj.setCommand(command)
	output = listFunctions.listToString(appleCommand)	
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setComment(output)
	return retObj	

def setPrivilegeSudo(dirPath, priv="775"):
	#sudo chmod -R 775 <path>
	retObj = funcReturn.funcReturn('setPrivilege')
	dirPath = dirPath.strip()
	appleCommand = ["sudo", "chmod", "-R",  priv, dirPath]
	output = listFunctions.listToString(appleCommand)	
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setComment(output)
	return retObj	
	
def setPrivilege(dirPath, priv="775"):
	#sudo chmod -R 775 <path>
	retObj = funcReturn.funcReturn('setPrivilege')
	dirPath = dirPath.strip()
	appleCommand = ["chmod", "-R",  priv, dirPath]
	output = listFunctions.listToString(appleCommand)	
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setComment(output)
	return retObj	
		
def setAttributes ( dirPath, own, group, priv ):
	retObj = funcReturn.funcReturn('setAttributes')
	dicCommand = {}
	og = own + ":" + group
	returnDic = {}
	retObj = setToUnLock(dirPath)
	returnDic['setToUnLock'] = retObj.getComment()
	retObj = setGroupOwner(dirPath, own, group)
	returnDic['setGroupOwner'] = retObj.getComment()
	retObj = setPrivilege(dirPath, priv)
	returnDic['setPrivilege'] = retObj.getComment()
	retObj.setComment(returnDic)
	retObj.setRetVal(0)
	return retObj
	
#set owner and posix recursively
#does not set the top of tree
def setPosixRec2 ( path, own, group, priv ):
	path = path.strip()
	own = own.strip()
	group = group.strip()
	
	ownID = pwd.getpwnam(own).pw_uid
	groupID = grp.getgrnam(group).gr_gid
	for root, dirs, files in os.walk(path): 
	  for d in dirs:  
		dirPath = os.path.join(root, d)
		if os.path.exists(dirPath):
			try:
				os.chmod(dirPath, priv)
			except:
				print "  unable to chmod " + d + " to privilege " + str(priv)
			try:
				os.chown(dirPath, ownID, groupID)
			except:
				print "unable to chown " + d + " to owner " +  str(ownID)
	 
	  for f in files:
		filePath = os.path.join(root, f)
		if os.path.exists(filePath):
			try:
				os.chmod(filePath, priv)
			except:
				print "unable to chmod file " + f + " to privilege " + str(priv)
			try:
				os.chown(filePath, ownID, groupID)
			except:
				print "unable to chown file " + f + " to owner " + str(ownID)

#set owner and posix recursively
#does not set the top of tree
def setPosixRec ( path, own, priv ):
	ownID = pwd.getpwnam(own).pw_uid
	groupID = -1
	for root, dirs, files in os.walk(path): 
	  for d in dirs:  
		dirPath = os.path.join(root, d)
		if os.path.exists(dirPath):
			try:
				os.chmod(dirPath, priv)
			except:
				print "  unable to chmod " + d + " to privilege " + str(priv)
			try:
				os.chown(dirPath, ownID, groupID)
			except:
				print "unable to chown " + d + " to owner " +  str(ownID)
	 
	  for f in files:
		filePath = os.path.join(root, f)
		if os.path.exists(filePath):
			try:
				os.chmod(filePath, priv)
			except:
				print "unable to chmod file " + f + " to privilege " + str(priv)
			try:
				os.chown(filePath, ownID, groupID)
			except:
				print "unable to chown file " + f + " to owner " + str(ownID)

def deleteFileOrFolder(topDirectory):
	uid = pwd.getpwnam("ladmin")[2]
	gid = grp.getgrnam("staff")[2]
	
	if os.path.exists(topDirectory):
		for root, dirs, files in os.walk(topDirectory, topdown=False):
			for name in files:
				path = os.path.join(root, name)				
				if os.path.exists(path):
					try:
						os.chown(path, uid, gid)
						os.remove(path)
					except:
						#print "deleting file Exception ",str(sys.exc_info()), path
						sys.exit(1)
			for name in dirs:
				path = os.path.join(root, name)			
				if os.path.exists(path):
					try:
						os.rmdir(path)	
					except:
						#print "deleting folder Exception ",str(sys.exc_info()), path
						sys.exit(1)
	else:
		print "given directory not found ", topDirectory

def makeDirectoryObj (dirPath):
	retObj=funcReturn.funcReturn('makeDirectoryObj')
	try:
		os.makedirs(dirPath)
		retObj.setRetVal(0)
		comment = dirPath + " created"
		retObj.setComment(comment)
	except OSError as exc:
		if exc.errno != errno.EEXIST:
			retObj.setRetVal(1)
			error = exc +  " - unable to make directories"
			retObj.setError(error )
		else:
			retObj.setRetVal(0)
			comment = dirPath + " already exists"
			retObj.setComment(comment)
	return retObj
	
def makeDirectory (dirPath):
	if not os.path.exists(dirPath):
		os.makedirs(dirPath)
		
def makeDirectory2 (dirPath):
	dict = {'function' : 'makeDirectory2'}
	dict['retVal']= 0
	if not os.path.exists(dirPath):
		try:
			os.makedirs(dirPath, 0755 );
			dict['retVal']= 0
			dict['comment']="made path"
		except:
			dict['retVal']= 1
			dict['comment']="error occurred"
			return dict
	else:
		dict['comment']="path exists"
	return dict

def makeDirectoryBash (dirPath):
	dict = {'function' : 'makeDirectoryBash'}
	dict['retVal']= 0
	dirPath = dirPath.strip()
	command = "/bin/mkdir " + dirPath 
	dict['command']=command
	if not os.path.exists(dirPath):
		retVal = comWrap.comWrap (command)
		#print (str(retVal))
		if os.path.isdir(dirPath):
			dict['retVal']= 0
			dict['comment']="made path"
		else:
			dict['retVal']= 1
			dict['comment']="error occurred"
			return dict
	else:
		dict['comment']="path exists"
	return dict

def makeDirectoryBashSudo (dirPath):
	retObj = funcReturn.funcReturn('makeDirectoryBash2')
	#print "dirPath:  " + dirPath
	dirPath = dirPath.strip()
	command = "sudo /bin/mkdir -p " + dirPath 
	retObj.setCommand(command)
	if not os.path.exists(dirPath):
		retObjCW = comWrap.comWrapString (command)
		retObj.setRetVal(retObjCW.getRetVal())
		#print (str(retVal))
	else:
		retObj.setRetVal(0)
		comment=="path exists"
		retObj.setComment(comment)
	return retObj
		
def makeDirectoryBash2 (dirPath):
	retObj = funcReturn.funcReturn('makeDirectoryBash2')
	#print "dirPath:  " + dirPath
	dirPath = dirPath.strip()
	command = "/bin/mkdir " + dirPath 
	retObj.setCommand(command)
	if not os.path.exists(dirPath):
		retVal = comWrap.comWrap (command)
		#print (str(retVal))
		if os.path.isdir(dirPath):
			retObj.setRetVal(0)
			comment="made path"
			retObj.setComment(comment)
		else:
			retObj.setRetVal(1)
			comment="error occurred"
			retObj.setComment(comment)
			return retObj
	else:
		comment=="path exists"
		retObj.setComment(comment)
	return retObj