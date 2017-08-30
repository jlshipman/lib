import os
import sys
import time
import fileFunctions
import listFunctions
import funcReturn
import comWrap
import stringFunctions
import timeFunc
import datetime
import paramiko
import select


def putCkSum(hostname, user, localPathSrc, remotePathDir, outputLogFile, stage, mode=0770):
	retObj = funcReturn.funcReturn('putCkSum')
	print "putCkSum"
	print "\thostname:                " + hostname
	print "\tuser:                    " + user
	print "\tlocalPathSrc:            " + localPathSrc
	print "\tremotePathDir:           " + remotePathDir
	print "\toutputLogFile:           " + outputLogFile
	print "\tstage:                   " + stage
	#if local file exists
	if fileFunctions.fileExist(localPathSrc):
		#create checksum based off of localPathSrc
		retObjFile=fileFunctions.checkSumObj(localPathSrc)
		CkSumRetVal=retObjFile.getRetVal()
		if CkSumRetVal == 0:
			ck = retObjFile.getStdout()
			print "\tck:  " + ck
			base = os.path.basename(localPathSrc)
			dir =  os.path.dirname(localPathSrc)
			curDir=os.getcwd()
			os.chdir(dir)
			localPathSrcCK = localPathSrc + ".ck"
			print "\tlocalPathSrcCK:  " + localPathSrcCK
			retObjFileCreate=fileFunctions.fileCreateWrite(localPathSrcCK, ck)
			if retObjFileCreate.getRetVal() == 0:
				#put ck on remote device
				base = os.path.basename(localPathSrc)
				remoteFile = remotePathDir + "/" + base + ".ck"
				print "\tremoteFile:  " + remoteFile
				retObjPut=put(hostname, user, localPathSrcCK, remoteFile, outputLogFile, stage, mode=0770)

				if retObjPut.getRetVal() == 0:
					#check CK put on remote server
					retObjStatCK = stat(hostname, user, remoteFile, outputLogFile, stage)
					if retObjStatCK.getRetVal() == 0:	

						#confirm size equivalency of remote and local files		
						results=retObjStatCK.getResult()
						size=results.st_size
						remoteSize=int(size)
						localSize=int(fileFunctions.fileSize(localPathSrcCK))
						if remoteSize == localSize:
							retObj.setRetVal(0)
						else:
							retObj.setError("remote ck, "+ remoteFile +  "- " + str(remoteSize) +" ,differs in size from local ck, " + localPathSrc +  "- " + str(localSize))
					else:		
						retObj.setError("remote did not receive file")
					
					#delete ck file after it has been sent
					fileFunctions.fileDelete(localPathSrcCK)	
				else:
					retObj.setError("local check file: " + localPathSrcCK + ", put failed.")
					return retObj		
			else:
				retObj.setError("local check file: " + localPathSrcCK + ", was not created.")	
				return retObj
		else:
			retObj.setError("problem creating check sum: " + localPathSrcCK)	
			return retObj			
	else:
		retObj.setError("local file: " + localPathSrc + ", does not exist.")	
		
	return retObj		
			
def put(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage, mode=0770):
	retObj = funcReturn.funcReturn('put')
	#if local file exists
	if fileFunctions.fileExist(localFilePath):
		############################template code - begin ############################ 
		if fileFunctions.fileExist(outputLogFile):
			fileFunctions.fileDelete (outputLogFile)
		fileFunctions.fileCreate(outputLogFile)
		os.chmod(outputLogFile, 0777)
		comments = ''
		ssh = paramiko.SSHClient() 
		paramiko.util.log_to_file(outputLogFile)
		try:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		except Exception:
			retObj.setError("set_missing_host_key_policy")
			retObj.setComment(comments)
			return retObj
		
		comments = comments + 'ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) \n'
		#In case the server's key is unknown,
		#we will be adding it automatically to the list of known hosts
		try:
			ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts")))			
		except Exception:
			retObj.setError("load_host_keys")
			retObj.setComment(comments)
			return retObj

		comments = comments + 'ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts"))) \n'
		try:
			ssh.connect(hostname,  username=user)
		except Exception:
			retObj.setError("connect")
			retObj.setComment(comments)
			return retObj

		comments = comments + 'ssh.connect(hostname,  username=user)  \n'
		try:
			sftp = ssh.open_sftp()
		except Exception:
			retObj.setError("ssh.open_sftp")
			retObj.setComment(comments)
			return retObj
			
		comments = comments + 'sftp = ssh.open_sftp()'	
		############################template code - end############################ 
		startTime = datetime.datetime.now()		
		try:
			sftp.put(localFilePath, remoteFilepath)
		except IOError, e:
			retObj.setError("sftp.put  " +str(e) )
			sftp.close()
			ssh.close()
			retObj.setComment(comments)
			return retObj	
		comments = comments + 'sftp.put(localFilePath, remoteFilepath)  \n'			
		endTime = datetime.datetime.now()	
		resultDict = timeFunc.timeDuration2 (endTime, startTime)
		try:	
			sftp.close()
			ssh.close()
		except Exception:
			retObj.setError("unable to close")
			retObj.setComment(comments)

		comments = comments + 'sftp.close();ssh.close()  \n'		
		#confirm sftp and ssh are closed.
		retObj.setComment(comments)
		retObjStat=stat(hostname, user, remoteFilepath, outputLogFile, stage)
		if retObjStat.getRetVal() == 0:	
		
			#confirm size equivalency of remote and local files
			resultFileProperties=retObjStat.getResult()	
			remoteSize=int(resultFileProperties.st_size)
			localSize=int(fileFunctions.fileSize(localFilePath))
			if remoteSize == localSize:
				resultDict['size']=int(remoteSize)
			else:
				retObj.setError("remote file, "+ remoteFile +  "- " + str(remoteSize) +", differs in size from local file, " + localFilePath +  "- " + str(localSize))
				return retObj	
		else:		
			retObj.setError("remote host did not receive file")
			return retObj	

		resultDict['hostname']=hostname
		resultDict['user']=user
		resultDict['localFilePath']=localFilePath
		resultDict['remoteFilepath']=remoteFilepath
		resultDict['outputLogFile']=outputLogFile
		resultDict['stage']=stage
		resultDict['mode']=str(mode)
		resultDict['fileProperties']=resultFileProperties
		retObj.setResult(resultDict)
		
		
		retObj.setRetVal(0)
	
	return retObj

def delete(hostname, user, localFilePath, remoteFilepath, outputLogFile, stage, mode=0770):
	retObj = funcReturn.funcReturn('delete')
	#if local file exists
	if fileFunctions.fileExist(localFilePath):
		############################template code - begin ############################ 
		if fileFunctions.fileExist(outputLogFile):
			fileFunctions.fileDelete (outputLogFile)
		fileFunctions.fileCreate(outputLogFile)
		os.chmod(outputLogFile, 0777)
		comments = ''
		ssh = paramiko.SSHClient() 
		paramiko.util.log_to_file(outputLogFile)
		try:
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		except Exception:
			retObj.setError("set_missing_host_key_policy")
			retObj.setComment(comments)
			return retObj
		
		comments = comments + 'ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) \n'
		#In case the server's key is unknown,
		#we will be adding it automatically to the list of known hosts
		try:
			ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts")))			
		except Exception:
			retObj.setError("load_host_keys")
			retObj.setComment(comments)
			return retObj

		comments = comments + 'ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts"))) \n'
		try:
			ssh.connect(hostname,  username=user)
		except Exception:
			retObj.setError("connect")
			retObj.setComment(comments)
			return retObj

		comments = comments + 'ssh.connect(hostname,  username=user)  \n'
		try:
			sftp = ssh.open_sftp()
		except Exception:
			retObj.setError("ssh.open_sftp")
			retObj.setComment(comments)
			return retObj
			
		comments = comments + 'sftp = ssh.open_sftp()'	
		############################template code - end############################ 
		startTime = datetime.datetime.now()		
		try:
			sftp.remove(remoteFilepath)
		except IOError, e:
			retObj.setError("sftp.remove  " +str(e) )
			sftp.close()
			ssh.close()
			retObj.setComment(comments)
			return retObj	
		comments = comments + 'sftp.remove(remoteFilepath)  \n'			
		endTime = datetime.datetime.now()	
		resultDict = timeFunc.timeDuration2 (endTime, startTime)
		try:	
			sftp.close()
			ssh.close()
		except Exception:
			retObj.setError("unable to close")
			retObj.setComment(comments)

		comments = comments + 'sftp.close();ssh.close()  \n'		
		#confirm sftp and ssh are closed.
		retObj.setComment(comments)
		retObjStat=stat(hostname, user, remoteFilepath, outputLogFile, stage)
		if retObjStat.getRetVal() == 0:	
		
			#confirm size equivalency of remote and local files
			resultFileProperties=retObjStat.getResult()	
			remoteSize=int(resultFileProperties.st_size)
			localSize=int(fileFunctions.fileSize(localFilePath))
			if remoteSize == localSize:
				resultDict['size']=int(remoteSize)
			else:
				retObj.setError("remote file, "+ remoteFile +  "- " + str(remoteSize) +", differs in size from local file, " + localFilePath +  "- " + str(localSize))
				return retObj	
		else:		
			retObj.setError("remote host did not receive file")
			return retObj	

		resultDict['hostname']=hostname
		resultDict['user']=user
		resultDict['localFilePath']=localFilePath
		resultDict['remoteFilepath']=remoteFilepath
		resultDict['outputLogFile']=outputLogFile
		resultDict['stage']=stage
		resultDict['mode']=str(mode)
		resultDict['fileProperties']=resultFileProperties
		retObj.setResult(resultDict)
		
		
		retObj.setRetVal(0)
	
	return retObj
	
def mkdir(hostname, user, remoteDirpath, outputLogFile, stage, mode=0770):
	retObj = funcReturn.funcReturn('mkdir')
	############################template code - begin############################ 
	if fileFunctions.fileExist(outputLogFile):
		fileFunctions.fileDelete (outputLogFile)
	fileFunctions.fileCreate(outputLogFile)
	os.chmod(outputLogFile, 0777)
	
	ssh = paramiko.SSHClient() 
	paramiko.util.log_to_file(outputLogFile)
	comment = ""
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		comment = comment + "ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy() \n"
	except Exception:
		retObj.setError("set_missing_host_key_policy")
		return retObj

	retObj.setComment(comment)
			
	#In case the server's key is unknown,
	#we will be adding it automatically to the list of known hosts
	try:
		ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts")))			
		comment = comment + "ssh.load_host_keys(os.path.expanduser... \n"
	except Exception:
		retObj.setError("load_host_keys")
		return retObj

	retObj.setComment(comment)
	
	try:
		ssh.connect(hostname,  username=user)
		comment = comment + "ssh.connect(hostname,  username=user) \n"
	except Exception:
		retObj.setError("connect")
		return retObj

	retObj.setComment(comment)
	
	try:
		sftp = ssh.open_sftp()
		comment = comment + "sftp = ssh.open_sftp() \n"
	except Exception:
		retObj.setError("ssh.open_sftp")
		return retObj

	retObj.setComment(comment)
	
	############################template code - end############################ 
	retStatObj=stat(hostname, user, remoteDirpath, outputLogFile, stage)		
	retVal = retStatObj.getRetVal()
	if retVal == 1:
		try:
			sftp.mkdir(remoteDirpath, mode=mode)
		except IOError, e:
			retObj.setError("sftp.mkdir  " +str(e) )
			return retObj		
		else:
			 result = 0
			 retObj.setComment("directory:  " + remoteDirpath + " created")
	else:
		result = 0
		retObj.setComment("directory:  " + remoteDirpath + " already exists")
		
	try:	
		sftp.close()
		ssh.close()
	except Exception:
		retObj.setError("unable to close")

	retObj.setRetVal(0)
	
	return retObj
		
def stat(hostname, user, dirFile, outputLogFile, stage):
	retObj = funcReturn.funcReturn('stat')

	if fileFunctions.fileExist(outputLogFile):
		fileFunctions.fileDelete (outputLogFile)
	fileFunctions.fileCreate(outputLogFile)
	os.chmod(outputLogFile, 0777)
	
	ssh = paramiko.SSHClient() 
	paramiko.util.log_to_file(outputLogFile)
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	except Exception:
		retObj.setError("set_missing_host_key_policy")
		return retObj
		
	#In case the server's key is unknown,
	#we will be adding it automatically to the list of known hosts
	try:
		ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts")))			
	except Exception:
		retObj.setError("load_host_keys")
		return retObj

	try:
		ssh.connect(hostname,  username=user)
	except Exception:
		retObj.setError("connect")
		return retObj

	try:
		sftp = ssh.open_sftp()
	except Exception:
		retObj.setError("ssh.open_sftp")
		return retObj
	############################template code - end############################ 		
	try:
		result=sftp.stat(dirFile)
	except IOError as e:
		retObj.setError("sftp.stat" + str(e))
		substring="No such file"
		if (substring in str(e)):
			retObj.setComment("directory or file:  " + dirFile + " does not exists")
		return retObj		
	
	try:	
		sftp.close()
		ssh.close()
	except Exception:
		retObj.setError("unable to close")

	retObj.setResult(result)
	retObj.setComment("directory or file:  " + dirFile + " exists")
	retObj.setRetVal(0)
	
	return retObj
	
def logonSftp(hostname, user, password=""):
	retObj = funcReturn.funcReturn('logon')
	if password == "":
		sftpLogon="sftp://" + user + "@" + hostname
	else:
		sftpLogon="sftp://" + user + ":" + password + "@" + hostname
		
	retObj.setRetVal(0)
	retObj.setResult(sftpLogon)
	return retObj
	
def checkSumRemoteCheck(hostname, user, remotePathDst, remotePathDstCK, localPathSrc, delete, stage, password=""):
	retObj = funcReturn.funcReturn('checkSumRemoteCheck')
	
	#get remoteFile
	base = os.path.basename(remotePathDst)
	dir =  os.path.dirname(remotePathDst)
	localDownPathFile = localPathSrc + "/" + base
	retObjGetFile=getFile(hostname, user, remotePathDst, localDownPathFile, stage, password)
	
	#get remoteFileCK
	base = os.path.basename(remotePathDstCK)
	dir =  os.path.dirname(remotePathDstCK)
	localDownPathCK = localPathSrc + "/" + base
	retObjGetCK=getFile(hostname, user, remotePathDstCK, localDownPathCK, stage, password)
	
	#read in remoteFileCK
	remoteCK=fileFunctions.readFirstLineFile(localDownPathCK)
	
	#create checksum of remoteFile
	retObjFile=fileFunctions.checkSumObj(localDownPathFile)
	localCK = retObjFile.getStdout()
	
	#compare two checksoms
	if localCK == remoteCK:
		retObj.setRetVal(0)

	retObj.setComment("local ck:  _" + localCK + "_  remote ck _" + remoteCK + "_")

 	#delete files if delete is set
	if delete == "yes":
		fileFunctions.fileDelete(localDownPathCK)
		fileFunctions.fileDelete(localDownPathFile)
	return retObj
	
def makeDir(hostname, user, remoteDirPath, stage, password=""):
	retObj = funcReturn.funcReturn('makeDir')
	fileStatObj=fileDirStat(hostname, user, remoteDirPath, stage, password)
	if fileStatObj.getFound () == 1:
		#lftp sftp://jshipman:"q1w2e3r4Q!W@E#R$"@css.larc.nasa.gov -e "mkdir test; bye"
		#lftp -u jshipman, sftp://css.larc.nasa.gov -e "mkdir test; bye"
		if password=="":
			sftpLogon="-u " + user + ","  + "empty " + "sftp://" + hostname
			sftpCode='"mkdir -p ' + remoteDirPath  + '; bye"'
			appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		else:
			sftpLogon="sftp://" + user + ":" + password + "@" + hostname
			sftpCode="mkdir -p " + remoteDirPath  + "; bye"
			appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		output = listFunctions.listToString(appleCommand)
		retObj = comWrap.comWrapRetObj(appleCommand)
		retObj.setName('makeDir')
		retObj.setComment(output)
		fileStat2Obj=fileDirStat(hostname, user, remoteDirPath, stage, password)
		if fileStat2Obj.getFound() == 0:
			retObj.setRetVal(0)
	else:
		retObj.setComment("directory already exists")
		retObj.setRetVal(0)
	return retObj
			
def getDirList(hostname, user, remotePathDst, listFile, stage, password=""):
	#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "ls; bye" 
	retObjLogon=logonSftp(hostname, user, password)
	sftpLogon=retObjLogon.getResult()
	sftpCode="ls; bye"
	appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
	output = listFunctions.listToString(appleCommand)
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setName('getDirList')
	retObj.setComment(output)
	return retObj

def putFileDirCheck(hostname, user, remotePathDst, localPathSrc, temp, stage, password=""):
	#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "put /scripts/nearLine/lib/unitTests/TEMP/txtfile_3_12_11_51"
	
	#if local file exists
	if fileFunctions.fileExist(localPathSrc):
	
		#check if localPathSrc is file
		if os.path.isfile(localPathSrc):
			retObj.setComment(localPathSrc + " is a file")
			#create local check sum
			retObjFile=fileFunctions.checkSumObj(localPathSrc)
			localCK = retObjFile.getStdout()
			remotePathDst = remotePathDst + ".ck"
			base = os.path.basename(localPathSrc)
			localDownPathCK = localPathDir + "/" + base + ".ck"
			##lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "get /mss/js/jshipman/archive1/txtfile_3_18_9_36.ck"
			retObjGetFile = getFile(hostname, user, remotePathDst, localDownPathCK, stage, password="")
			getFileRetVal = retObjGetFile.getRetVal()
			
			#checksum does not exist thus no file has been uploaded
			if getFileRetVal == 1:
				checkSumCheck = 0
			else:
				#read in remoteFileCK
				remoteCK=fileFunctions.readFirstLineFile(localDownPathCK)
	
				#compare two checksoms
				if localCK == remoteCK:
					#checksum are the same 
					#files are the same
					checkSumCheck = 1
					retObj.setRetVal(0)
					retObj.setComment("check sums matched, no need to put file")
				else:
					#checksums are different
					#new file to be uploaded with same name
					checkSumCheck = 0
		else:
			checkSumCheck = 0
			
		if checkSumCheck == 0:
			#sftp put to remote server
			retObjLogon=logonSftp(hostname, user, password)
			sftpLogon=retObjLogon.getResult()
			sftpCode="put " + " -O "  + remotePathDst + " " + localPathSrc + "; bye"
			appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		
			startTime = datetime.datetime.now()
			retObj = comWrap.comWrapRetObj(appleCommand)
			endTime = datetime.datetime.now()
			resultDict = timeFunc.timeDuration2 (endTime, startTime)
			retObj.setResult(resultDict)
		
			retObj.setName('putFileDir')
			output = listFunctions.listToString(appleCommand)
			retObj.setComment(output)
	
			#check file put on remote server
			base = os.path.basename(localPathSrc)
			remoteFile = remotePathDst + "/" + base
			retObjStatTar = fileDirStat(hostname, user, remoteFile, stage, password)
			if retObjStatTar.getRetVal() == 0:	
			
				#confirm size equivalency of remote and local files
				results=retObjStatTar.getResult()
				remoteSize=int(results['size'])
				localSize=int(fileFunctions.fileSize(localPathSrc))
				if remoteSize == localSize:
					retObj.setRetVal(0)
					resultDict['size']=int(results['size'])
				else:
					retObj.setRetVal(1)
					retObj.setError("remote file, "+ remoteFile +  "- " + str(remoteSize) +" ,differs in size from local file, " + localPathSrc +  "- " + str(localSize))
			else:		
				retObj.setRetVal(1)
				retObj.setError("remote host did not receive file")
			
	else:
		retObj = funcReturn.funcReturn('putFileDir')
		retObj.setRetVal(1)
		retObj.setError("local file, " + localPathSrc + ", does not exist.")

	return retObj
		
def putFileDir(hostname, user, remotePathDst, localPathSrc, stage, password=""):
	#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "put /scripts/nearLine/lib/unitTests/TEMP/txtfile_3_12_11_51"
	
	#if local file exists
	if fileFunctions.fileExist(localPathSrc):
	
		#sftp put to remote server
		retObjLogon=logonSftp(hostname, user, password)
		sftpLogon=retObjLogon.getResult()
		sftpCode="put " + " -O "  + remotePathDst + " " + localPathSrc + "; bye"
		appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		
		startTime = datetime.datetime.now()
		retObj = comWrap.comWrapRetObj(appleCommand)
		endTime = datetime.datetime.now()
		resultDict = timeFunc.timeDuration2 (endTime, startTime)
		retObj.setResult(resultDict)
		
		retObj.setName('putFileDir')
		output = listFunctions.listToString(appleCommand)
		retObj.setComment(output)
	
		#check file put on remote server
		base = os.path.basename(localPathSrc)
		remoteFile = remotePathDst + "/" + base
		retObjStatTar = fileDirStat(hostname, user, remoteFile, stage, password)
		if retObjStatTar.getRetVal() == 0:	
			
			#confirm size equivalency of remote and local files
			results=retObjStatTar.getResult()
			remoteSize=int(results['size'])
			localSize=int(fileFunctions.fileSize(localPathSrc))
			if remoteSize == localSize:
				retObj.setRetVal(0)
				resultDict['size']=int(results['size'])
			else:
				retObj.setRetVal(1)
				retObj.setError("remote file, "+ remoteFile +  "- " + str(remoteSize) +" ,differs in size from local file, " + localPathSrc +  "- " + str(localSize))
		else:		
			retObj.setRetVal(1)
			retObj.setError("remote host did not receive file")
			
	else:
		retObj = funcReturn.funcReturn('putFileDir')
		retObj.setRetVal(1)
		retObj.setError("local file, " + localPathSrc + ", does not exist.")

	return retObj

def putCheckSum(hostname, user, remotePathDst, localPathSrc, stage, password=""):
	#create checksum based off of localPathSrc
	retObjFile=fileFunctions.checkSumObj(localPathSrc)
	ck = retObjFile.getStdout()
	base = os.path.basename(localPathSrc)
	dir =  os.path.dirname(localPathSrc)
	curDir=os.getcwd()
	os.chdir(dir)
	localPathSrcCK = localPathSrc + ".ck"
	retObjFileCreate=fileFunctions.fileCreateWrite(localPathSrcCK, ck)

	#if local ck file exists
	if fileFunctions.fileExist(localPathSrcCK):

		#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "put /scripts/nearLine/lib/unitTests/TEMP/txtfile_3_12_11_51"
		#put ck on remote device
		retObjLogon=logonSftp(hostname, user, password)
		sftpLogon=retObjLogon.getResult()
		sftpCode="put " + " -O "  + remotePathDst + " " + localPathSrcCK + "; bye"
		appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		retObj = comWrap.comWrapRetObj(appleCommand)
		output = listFunctions.listToString(appleCommand)		
		retObj.setComment(output)

		#check CK put on remote server
		base = os.path.basename(localPathSrc)
		remoteFile = remotePathDst + "/" + base + ".ck"
		retObjStatCK = fileDirStat(hostname, user, remoteFile, stage, password)
		if retObjStatCK.getRetVal() == 0:	

			#confirm size equivalency of remote and local files		
			results=retObjStatCK.getResult()
			remoteSize=int(results['size'])
			localSize=int(fileFunctions.fileSize(localPathSrcCK))
			if remoteSize == localSize:
				retObj.setRetVal(0)
			else:
				retObj.setRetVal(1)
				retObj.setError("remote ck, "+ remoteFile +  "- " + str(remoteSize) +" ,differs in size from local ck, " + localPathSrc +  "- " + str(localSize))
		else:		
			retObj.setRetVal(1)
			retObj.setError("remote did not receive file")
	
		#delete ck file after it has been sent
		fileFunctions.fileDelete(localPathSrcCK)
		
	else:
		retObj = funcReturn.funcReturn('putCheckSum')
		retObj.setRetVal(1)
		retObj.setError("local Ck file, " + localPathSrcCK + ", does not exist.")

	return retObj
						
def fileDirStat(hostname, user, remotePathDst, stage, password=""):
	#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "ls; bye" 
	retObjLogon=logonSftp(hostname, user, password)
	if password=="":
		sftpLogon="-u " + user + ", "  + "sftp://" + hostname
	else:
		sftpLogon="sftp://" + user + ":" + password + "@" + hostname
		
	base = os.path.basename(remotePathDst)
	dir =  os.path.dirname(remotePathDst)
	
	sftpCode="ls " + dir + "; bye"

	appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
	output = listFunctions.listToString(appleCommand)
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setName("fileDirStat")
	retObj.setComment(output)
	if retObj.getRetVal() == 0:
		stdout = retObj.getStdout ()
		output = listFunctions.stringToList (stdout, "\n")
		
		for o in output:	
			if o != "":
				fileStatsObj = fileFunctions.fileStatsFromString(o)
				resultDict = fileStatsObj.getResult()
				filename = resultDict['filename']
				if filename == base:
					find = o
					retObj.setFound(0)
				
		if retObj.getFound() == 0:
			fileStatsObj = fileFunctions.fileStatsFromString(find)
			resultDict = fileStatsObj.getResult()
			retObj.setResult(resultDict)
			retObj.setRetVal(0)
			
	return retObj

#test file to see if it has been put to tape
def fileDirStatSSH ( filename, remoteHost, user, stage , password=""):
	retObj = funcReturn.funcReturn('fileDirStatSSH')
	#ssh -q jshipman@css.larc.nasa.gov masls -l1 filename
	logon = user + "@" + remoteHost
	appleCommand = ["ssh", "-q", logon, "masls", "-l1", filename ]
	output = listFunctions.listToString(appleCommand)
	retObj = comWrap.comWrapRetObj(appleCommand)
	retObj.setName('fileDirStat2')
	retObj.setComment(output)
	stdout = retObj.getStdout()
	if retObj.getRetVal() == 0:
		stdout = retObj.getStdout()
		output = listFunctions.stringToList (stdout, "\n")
		for o in output:	
			#print "\t\t\to:  "+ o
			if o != "":
				fileStatsObj = fileFunctions.fileStatsNoGroupsFromString(o)
				resultDict = fileStatsObj.getResult()
				filenameStat = resultDict['filename']
				#print "\t\t\tfilename:  "+ filename
				#print "\t\t\tfilenameStat:  "+ filenameStat
				if filenameStat == filename:
					find = o
					#print "\t\t\tfilenameStat == filename"
					retObj.setFound(0)
			
		if retObj.getFound() == 0:
			retObj.setRetVal(0)
		else:
			retObj.setRetVal(1)
	return retObj
		
def getFile(hostname, user, remotePathDst, localPathSrc, stage, password=""):

	#if remote file exists
	retObjStat = fileDirStat(hostname, user, remotePathDst, stage, password)
	if retObjStat.getRetVal() == 0:
		#lftp sftp://jshipman:"nhy6mju7NHY^MJU&"@css.larc.nasa.gov -e "get /mss/js/jshipman/archive1/txtfile_3_18_9_36.ck"
		#get file on remote device
		retObjLogon=logonSftp(hostname, user, password)
		sftpLogon=retObjLogon.getResult()
		sftpCode="set xfer:clobber on; get " + remotePathDst + " -o "  + localPathSrc + "; bye"
		appleCommand = ["lftp", sftpLogon, "-e", sftpCode]
		retObj = comWrap.comWrapRetObj(appleCommand)
		output = listFunctions.listToString(appleCommand)		
		retObj.setComment(output)
		
		#confirm size equivalency of remote and local files
		results=retObjStat.getResult()
		remoteSize=int(results['size'])
		localSize=int(fileFunctions.fileSize(localPathSrc))
		if remoteSize == localSize:
			retObj.setRetVal(0)
		else:
			retObj.setRetVal(1)
			retObj.setError("remote file, "+ remotePathDst +  "- " + str(remoteSize) +", differs in size from local file, " + localPathSrc +  "- " + str(localSize))
	else:
		retObj = funcReturn.funcReturn('getFile')
		retObj.setRetVal(1)
		retObj.setError("remote file, " + remoteFile + ", does not exist.")

	return retObj
	