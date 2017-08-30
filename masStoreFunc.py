import sys, os
sys.path.append('lib')
import commandwrapper 
import string
import fileFunctions 
import listFunctions
import timeFunc
import datetime 
import time
import comWrap
import funcReturn
import pwd
import paramiko
import select


def putSSH(remoteHost, user, localFilePath, remoteFilepath, outputLogFile, stage, passwd = "", mode=0770):
	retObj = funcReturn.funcReturn('putSSH')
	#ssh -q jshipman@css-10g.larc.nasa.gov masput - css-file-name <local-file-name
	
	if passwd == "":
		logon = user + "@" + remoteHost
		sshCommand = "sudo -u ladmin ssh -q " + logon + " masput - " + remoteFilepath + " < " + localFilePath
	else:
		logon = user + "@" + remoteHost + ":" + passwd
		sshCommand = "sudo -u ladmin ssh -q " + logon + " masput - " + remoteFilepath + " < " + localFilePath

	startTime = datetime.datetime.now()
	retObj = comWrap.comWrapString(sshCommand)
	endTime = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (endTime, startTime)
	
	resultDict = {}
	resultDict['seconds'] = timeDict['seconds']
	retObj.setName('putSSH')
	retObj.setCommand(sshCommand)
	
	resultDict['hostname']=remoteHost
	resultDict['user']=user
	resultDict['localFilePath']=localFilePath
	resultDict['remoteFilepath']=remoteFilepath
	resultDict['outputLogFile']=outputLogFile
	resultDict['stage']=stage
	resultDict['mode']=str(mode)
	resultDict['fileProperties']=""
	if retObj.getRetVal() == 0:
		sshCommand = "sudo -u ladmin ssh -q " + logon + " masls -al1 " + remoteFilepath
		retObjSSHStat = comWrap.comWrapString(sshCommand)
		if retObjSSHStat.getRetVal() == 0:
			retObjStatFile = fileFunctions.fileStatsNoGroupsFromString(retObjSSHStat.getStdout())
			resultFileProperties = retObjStatFile.getResult()
			resultDict['fileProperties']=resultFileProperties	
		else:
			retObj.setRetVal(1)
			retObj.setError("problem with stat command")
			retObj.setCommand(sshCommand)
	else:	
		retObj.setRetVal(1)
		retObj.setError("problem with ssh command")
	retObj.setResult(resultDict)
		
	return retObj
	
def checkSum(hostname, user, dirFile, outputLogFile, stage): 
	retObj = funcReturn.funcReturn('checkSum')

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

	############################template code - end############################ 		
	stdin, stdout, stderr = ssh.exec_command('"masget ' +  dirFile + ' - | sum"')
	print "stdin:  " + str(stdin.channel.recv(1024),)
	print "stdout:  " + str(stdout.channel.recv(1024),)
	print "stderr:  " + str(stderr.channel.recv(1024),) 
	output = ""
	# Wait for the command to terminate
	while not stdout.channel.exit_status_ready():
		# Only print data if there is data to read in the channel
		if stdout.channel.recv_ready():
			rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
			if len(rl) > 0:
				# Print data from stdout
				output = str(stdout.channel.recv(1024),)
				
	retObj.setStdout(output.strip())
	try:	
		ssh.close()
	except Exception:
		retObj.setError("unable to close")

	if output != "":
		stdout = retObj.getStdout()
		retObj.setRetVal(0)
	else:
		retObj.setRetVal(1)
	
	return retObj
	
def checkTape(hostname, user, dirFile, outputLogFile, stage):
	retObj = funcReturn.funcReturn('checkTape')
	#print "checkTape"
	#print "outputLogFile:   "   + outputLogFile
	if fileFunctions.fileExist(outputLogFile):
		fileFunctions.fileDelete (outputLogFile)
	fileFunctions.fileCreate(outputLogFile)
	os.chmod(outputLogFile, 0777)
	
	ssh = paramiko.SSHClient()
	#print "after chmod"
	paramiko.util.log_to_file(outputLogFile)
	comment = ""
	try:
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		newComment =  "ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy() \n"
		#print newComment
		comment = comment + newComment
	except Exception:
		retObj.setError("set_missing_host_key_policy")
		return retObj

	#print "after host key"
	retObj.setComment(comment)
			
	#In case the server's key is unknown,
	#we will be adding it automatically to the list of known hosts
	try:
		ssh.load_host_keys(os.path.expanduser(os.path.join("/Users/ladmin/", ".ssh", "known_hosts")))			
		newComment =  "ssh.load_host_keys(os.path.expanduser... \n"
		comment = comment + newComment
	except Exception:
		retObj.setError("load_host_keys")
		return retObj

	retObj.setComment(comment)
	
	try:
		ssh.connect(hostname,  username=user)
		newComment =  "ssh.connect(hostname,  username=user) \n"
		#print newComment
		comment = comment + newComment
	except Exception:
		retObj.setError("connect")
		return retObj

	retObj.setComment(comment)
	
	try:
		sftp = ssh.open_sftp()
		newComment =  "sftp = ssh.open_sftp() \n"
		#print newComment
		comment = comment + newComment
	except Exception:
		retObj.setError("ssh.open_sftp")
		return retObj

	retObj.setComment(comment)

	############################template code - end############################ 		
	stdin, stdout, stderr = ssh.exec_command("masls -lm " +  dirFile)
	
	output = ""
	# Wait for the command to terminate
	while not stdout.channel.exit_status_ready():
		# Only print data if there is data to read in the channel
		if stdout.channel.recv_ready():
			rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
			if len(rl) > 0:
				# Print data from stdout
				output = str(stdout.channel.recv(1024),)
				
	retObj.setStdout(output.strip())
	try:	
		ssh.close()
	except Exception:
		retObj.setError("unable to close")

	if output != "":
		stdout = retObj.getStdout()
		output = listFunctions.stringToList (stdout, "\n")
		for o in output:	
			#print "\t\t\to:  "+ o
			if o != "":
				fileStatsObj = fileFunctions.fileStatsNoGroupsFromString(o)
				resultDict = fileStatsObj.getResult()
				filenameStat = resultDict['filename']
				#print "\t\t\tdirFile:  "+ dirFile
				#print "\t\t\tfilenameStat:  "+ filenameStat
				if filenameStat == dirFile:
					find = o
					#print "\t\t\tfilenameStat == filename"
					retObj.setFound(0)
			
		if retObj.getFound() == 0:
			fileStatsObj = fileFunctions.fileStatsNoGroupsFromString(find)
			resultDict = fileStatsObj.getResult()
			#print "\t\t\tresultDict:  " + str(resultDict)
			posix = resultDict['posix']
			charResult =  posix[0]
			#print "\t\t\tcharResult:  "+ charResult
			if ( charResult == 'M' or charResult == 'm' ):
				retObj.setRetVal(0)
			else:
				retObj.setRetVal(1)
	
	return retObj
	
def recursiveListing (path, OutputFile):
	dict = {
	'function' : 'recursiveListing',
	'comment' : "",
	'error' : "",
	'retVal' : 0
	}
	print path
	print OutputFile
	masCommand = '/usr/local/bin/masls -R1  ' + path
	dict['masCommand']=masCommand
	result = comWrap.comWrap (masCommand)
#	copyErrorStr="No such file or directory"
# 	errorCheck = OutputFile.find(copyErrorStr)
# 	if errorCheck != -1 :
# 		dict['retVal'] = 1
# 		dict['error'] = copyErrorStr
	return dict
		
def masStoreDelayCheck ( startHour = 14, downTimeHours = 8 ):
	minute = 60 #seconds
	fiveMin = minute * 5
	hour = 60 * minute
	waitTime=fiveMin
	numWeekDay=datetime.datetime.today().weekday()
	now = datetime.datetime.now()
	hoursTilWed = startHour - now.hour
	if ( numWeekDay == 1 and hoursTilWed <= 0 ) :			
		hourDelay = downTimeHours
		secDelay = int (hour * hourDelay)
		print "sec delay:  " + str(secDelay)
		time.sleep (secDelay)
		
def masStoreDelay ( startHour = 15, downTimeHours = 7 ):
	minute = 60 #seconds
	fiveMin = minute * 5
	hour = 60 * minute
	waitTime=fiveMin
	numWeekDay=datetime.datetime.today().weekday()
	now = datetime.datetime.now()
	hoursTilWed = startHour - now.hour
	if not (numWeekDay == 1 and hoursTilWed <= 0 ) :			
		time.sleep (waitTime)
		print "waitTime:  " + str(waitTime)
	else:
		hourDelay = downTimeHours
		secDelay = int (hour * hourDelay)
		print "sec delay:  " + str(secDelay)
		time.sleep (secDelay)

def tarMasPut (item2Tar, cssArchive, tarErrorFile):
	dict = {'function' : 'tarMasPut'}
	if os.path.exists(tarErrorFile):
		os.unlink(tarErrorFile)
	errorDirPath = os.path.dirname(tarErrorFile)
	massPutErrorFile = errorDirPath + "/masPutErrorFile.txt"
	if os.path.exists(massPutErrorFile):
		os.unlink(massPutErrorFile)
	#command='/usr/bin/tar -cf - ' + item2Tar + ' 2> ' + tarErrorFile + ' | gzip -1 | /usr/local/bin/masput - ' + cssArchive + ' 2> ' + massPutErrorFile
	command='/usr/bin/tar -cf - ' + item2Tar + ' 2> ' + tarErrorFile +  ' | /usr/local/bin/masput - ' + cssArchive + ' 2> ' + massPutErrorFile
	#print command
	result=comWrap.comWrap (command)
	if os.path.exists(tarErrorFile):
		lines = 0
		f = open(tarErrorFile, 'r')
		lines = f.readlines()
		f.close()
		f = open(tarErrorFile, "w")
		for line in lines:
			if line!="tar: Removing leading '/' from member names"+"\n":
				f.write(line)
		f.close()
		with open(tarErrorFile) as fin:
			lines = sum(1 for line in fin)	
	 	if lines > 0:
			f = open(tarErrorFile, 'r')
			error = f.read().strip()
			f.close
			dict['function2'] = ''
			dict['error'] = error
			dict['error2'] = ''
			dict['function2Command'] = ''
			dict['retVal'] = 1
			dict['result2'] = ''
			return(dict)
	if os.path.exists(massPutErrorFile):
		lines = 0
		with open(massPutErrorFile) as fin:
			lines = sum(1 for line in fin)	
	 	if lines > 0:
			f = open(massPutErrorFile, 'r')
			error = f.read().strip()
			f.close
			dict['function2'] = ''
			dict['error'] = error
			dict['error2'] = ''
			dict['function2Command'] = ''
			dict['retVal'] = 1
			dict['result2'] = ''
			return(dict)	
		
	resultDict=masDirFileExists (cssArchive, errorDirPath)
	dict['function2'] = 'masDirFileExists'
	dict['error'] = resultDict['error']
	dict['error2'] = resultDict['error2']
	dict['function2Command'] = resultDict['command']
	dict['retVal'] = resultDict['retVal']
	dict['result2'] = resultDict['result']
	return(dict)
	
def masTapeCheck (archive):
	dict = {'function' : 'masTapeCheck'}
	masCommand = '/usr/local/bin/masls -alm  ' + archive
	#print masCommand
	dict['command']= masCommand
	command = commandwrapper.WrapCommand (masCommand)
	resultString = command ()
	#print resultString
	result = resultString.rstrip().split()
	#print "masCommand:  " + str(masCommand)
	dict['result']= str(result)
	firstEntry = result[0]
	firstChar  = firstEntry[0]
	dict['firstChar']= str(firstChar)
	#where "-" is file on disk cache only, 
	#"m" is file on disk cache and on tape, 
	#and "M" is file on tape only. 
	return dict
 
def masTapeCheck3 (archive):
	dict = {'function' : 'masMkdir'}
	masCommand = '/usr/local/bin/masls -alm  ' + archive
	dict['command']= masCommand
	command = commandwrapper.WrapCommand (masCommand)
	resultString = command ()
	#print "resultString:  " + str(resultString)
	result = resultString.rstrip().split()
	#print "result:  " + str(result)	
	#print "masCommand:  " + str(masCommand)
	copyErrorStr="No such file or directory"
	output=str(resultString)
	#print output
	errorCheck = output.find(copyErrorStr)
	if str(resultString) == "" :
		dict['retVal'] = 1
		dict['error'] = copyErrorStr
	elif errorCheck == -1:
		dict['retVal'] = 0
		dict['result']= str(result)
		firstEntry = result[0]
		firstChar  = firstEntry[0]
		dict['firstChar']= str(firstChar)
		#where "-" is file on disk cache only, 
		#"m" is file on disk cache and on tape, 
		#and "M" is file on tape only. 
	else:
		dict['retVal'] = 1
		dict['error'] = copyErrorStr
	return dict
	
def masListing (archive):
	 masCommand = '/usr/local/bin/masls -1  ' + archive
	 command = commandwrapper.WrapCommand (masCommand)
	 result = command ()
	 return result
	 		
def masCSSfileSize (file):
	#cssBytes=`/usr/local/bin/masls -al  "$dmss_split" | awk '{print $4}'`
	command = "/usr/local/bin/masls -al " + file + " | awk '{print $4}' "
	retVal=comWrap.comWrap (command)
	if retVal[0]==['']:
		return(0)
	else:
		return(retVal[0])	
	
def masMkdir ( cssDir, outputFile ):
	dict = {'function' : 'masMkdir'}
	command = "/usr/local/bin/masmkdir -p " + cssDir + " 2> " + outputFile
	errorDirPath = os.path.dirname(outputFile)
	dict['command']= command
	result=comWrap.comWrap (command)
	resultDict=masDirFileExists(cssDir, errorDirPath)
	dict['function2'] = 'masDirFileExists'
	dict['error'] = resultDict['error']
	dict['error2'] = resultDict['error2']
	dict['function2Command'] = resultDict['command']
	dict['retVal'] = resultDict['retVal']
	dict['result2'] = resultDict['result']
	return(dict)

def masTapeCheck2 (archive, errorDirPath ):
	dict = {'function' : 'masTapeCheck2'}
	errorFile = errorDirPath + "/fileMasTapeCheck2Error.txt"
	outputFile = errorDirPath + "/fileMasTapeCheck2Output.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)	
	masCommand = '/usr/local/bin/masls -alm  ' + archive + " 2> " + errorFile  + " > " + outputFile
	dict['command']= masCommand
	result=comWrap.comWrap (masCommand)
	f = open(errorFile, 'r')
	error = f.read()
	f.close
	
	copyErrorStr="No such file or directory"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dictResult['firstChar'] = ""
		dict['retVal']= 0
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
		
	copyErrorStr="nodename nor servname provided, or not known"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
	else:
		dict['retVal']= 0
		dict['error']= "none"
		dict['error2']="none"	
		#split on spaces 
		
		#read first line
		f = open(outputFile, 'r')
		firstLine = f.readline()
		f.close
		
		result = firstLine.rstrip().split()
		#print "masCommand:  " + str(masCommand)
		dict['result']= str(result)
		firstEntry = result[0]
		firstChar  = firstEntry[0]
		dict['firstChar']= str(firstChar)
		#where "-" is file on disk cache only, 
		#"m" is file on disk cache and on tape, 
		#and "M" is file on tape only. 
		return dict
	
def masDirFileExists ( cssDir, errorDirPath ):
	dict = {'function' : 'masDirFileExists'}
	cssDir = cssDir.rstrip("/")
	basePath = os.path.basename(cssDir) 
	dirPath = os.path.dirname(cssDir)
	errorFile = errorDirPath + "/fileMasLsError.txt"
	outputFile = errorDirPath + "/fileMasLsOutput.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -l1 " + dirPath + "/" + basePath + " 2> " + errorFile  + " > " + outputFile
	#print "command:  " + command
	dict['command']= command
	result=comWrap.comWrap (command)
	dict['result']= result
	dict['remoteFileSize']=0
	f = open(errorFile, 'r')
	error = f.read()
	f.close
	
	copyErrorStr="No such file or directory"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
		
	copyErrorStr="nodename nor servname provided, or not known"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
	else:
		dict['retVal']= 0
		dict['error']= "none"
		dict['error2']="none"	
		#split on spaces 
		
		#read first line
		f = open(outputFile, 'r')
		firstLine = f.readline()
		f.close
		
		#print "firstLine:  " + firstLine
		lineList = firstLine.split()
		#print "lineList:  " + str(lineList)
		if (len(lineList) > 4):
			remoteFileSize = int(lineList[3])
			dict['remoteFileSize']=remoteFileSize	
			
		#read in all lines
		f = open(outputFile, 'r')
		lines = f.readlines()
		f.close()
		dict['lines']= lines
		return dict
					
def masDirListing ( cssDir, errorDirPath ):
	dict = {'function' : 'masDirListing'}
	cssDir = cssDir.rstrip("/")
	errorFile = errorDirPath + "/errorDirMasLs.txt"
	outputFile = errorDirPath + "/outputDirMasLs.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -1 " + cssDir + "/" + " 2> " + errorFile + "  > " + outputFile 
	dict['command']= command
	result=comWrap.comWrap (command)
	dict['result']= result
	
	f = open(errorFile, 'r')
	output = f.read()
	f.close
	
	copyErrorStr="No such file or directory"
	errorCheck = output.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= cssDir + " does not exist"
		dict['error2']= output.strip()
		return dict
		
	copyErrorStr="nodename nor servname provided, or not known"
	errorCheck = output.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= output.strip()
		return dict
	else:
		dict['retVal']= 0
		dict['error']= "none"
		dict['error2']="none"	
		listDirContents = listFunctions.listFromFile(outputFile)
		dict['listDirContents']=listDirContents
		return dict
				
def masPutFunc ( file, cssPath , errorFile ):
	dict = {'function' : 'masPutFunc'}
	dict['function2'] = 'masDirFileExists'
	errorDirPath = os.path.dirname(errorFile)
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput " + file + " " + cssPath + " 2> " + errorFile
	dict['command']= command
	#print command
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	#print "cssSplitPath:  " + cssSplitPath
	#print "command:  " + command
	result=comWrap.comWrap (command)
	f = open(errorFile, 'r')
	output = f.read()
	f.close
	copyErrorStr="No such file or directory"
	errorCheck = output.find(copyErrorStr)
	if errorCheck == -1:
		dict['retVal']= 0
		dict['result']= result
		resultDict=masDirFileExists (cssSplitPath, errorDirPath)	
		dict['error'] = resultDict['error'] + " - file exist error"
		dict['function2Command'] = resultDict['command']
		dict['retVal'] = resultDict['retVal']
		dict['result2'] = resultDict['result']
	else:
		dict['retVal']= 1
		dict['error']= copyErrorStr + " - masput error"
	return(dict)

def masPutDelay ( file, cssPath , errorFile ):
	dict = {'function' : 'masPutDelay'}
	dict['function2'] = 'masDirFileExists'
	startTime = datetime.datetime.now()
	errorDirPath = os.path.dirname(errorFile)
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput " + file + " " + cssPath + " 2> " + errorFile
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath	
	dict['command']= command
	
	count=1
	result=1	
	while (count < 4 and result == 1):
		result=comWrap.comWrap (command)
		f = open(errorFile, 'r')
		output = f.read()
		f.close
		copyErrorStr="No such file or directory"
		errorCheck = output.find(copyErrorStr)
		if errorCheck == -1:
			endTime = datetime.datetime.now()
			timeDict = timeFunc.timeDuration2 (endTime, startTime)
			dict['runTotalSeconds'] = timeDict['seconds']
			dict['runHours'] = timeDict['printHours']
			dict['runMins'] = timeDict['printMins']
			dict['result']= 0
			resultDict=masDirFileExists (cssSplitPath, errorDirPath)			
			dict['error'] = resultDict['error'] + " - file exist error"
			dict['function2Command'] = resultDict['command']
			dict['retVal'] = resultDict['retVal']
			dict['result2'] = resultDict['result']
		else:
			dict['retVal']= 1
			dict['result']= 1
			dict['error']= copyErrorStr + " - masput error"
			
		count = count + 1
		if (result == 1):
			masStoreDelay()	
			
	return(dict)
	
def masPutDelay2 ( file, cssPath , errorFile, count=1 ):
	dict = {'function' : 'masputDelay2'}
	dict['function2'] = 'masDirFileExists'
	dict['result2'] = ""
	dict['function2Command'] = "none"
	startTime = datetime.datetime.now()
	errorDirPath = os.path.dirname(errorFile)
	if os.path.exists(errorFile):
		os.unlink(errorFile)
	command = "/usr/local/bin/masput - "  + cssPath + " 2> " + errorFile + " < "+ file 
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	
	dict['command']= command
	
	count=1
	result=1
	oneSec=1

	while (count < 4 and result == 1):
		masStoreDelayCheck()
		result=comWrap.comWrap (command)
		if os.path.exists(errorFile):
			f = open(errorFile, 'r')
			output = f.read()
			f.close
		else:
			output = ""
		copyErrorStr="No such file or directory"
		errorCheck = output.find(copyErrorStr)	
		if errorCheck == -1:
			#masput produced no error
			
			#check if remote file exists
			resultDict=masFileExists (cssPath, errorDirPath)
			
			dict['error'] = resultDict['error'] + " - file exist error"
			dict['function2Command'] = resultDict['command']
			remoteFileSize = resultDict['remoteFileSize']
			localFileSize=os.path.getsize(file)
			if (remoteFileSize == localFileSize):
				#sizes of remote and local files are equal
				dict['retVal'] = resultDict['retVal']
				dict['result2'] = resultDict['result']
				result=0
			else:
				#sizes of remote and local files are not equal
				result=1
				dict['retVal']=1				
				dict['error'] = " remote file size: _" + str(remoteFileSize) + "_ does not equal local file size:  _" + str(localFileSize) + "_"
		else:
			#directory on MSS does not exist
			#print "directory on MSS does not exist"
			result=1
			dict['retVal']= 1
			dict['error']= copyErrorStr + " - masput error"
			cssDirName=os.path.dirname(cssPath)
			errorMasFileMkdir=errorDirPath + "/errorMasFileMkdir.txt"
			resultDict2=masMkdirDelay(cssDirName,errorMasFileMkdir)
			result=resultDict2['retVal']
			if result != 0:
				dict['function2'] = 'masMkdirDelay'
				dict['command'] = resultDict['command']
				dict['error']= resultDict['error2']
			waitTime=oneSec	
			
		count = count + 1
		if (result == 1):
			masStoreDelay()				
	endTime = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (endTime, startTime)
	dict['runTotalSeconds'] = timeDict['seconds']
	dict['runHours'] = timeDict['printHours']
	dict['runMins'] = timeDict['printMins']			
	dict['result']= result
	return(dict)
	
def masMkdirDelay ( cssDir, outputFile ):
	dict = {'function' : 'masMkdirDelay'}
	command = "/usr/local/bin/masmkdir -p " + cssDir + " 2> " + outputFile
	dict['function2'] = 'masDirFileExists'
	
	count=1
	result=1
	while (count < 4 and result == 1):
		#currently errorFile is not check neither is
		#result at this point
		result=comWrap.comWrap (command)
		dict['result']=result
		
		f = open(outputFile, 'r')
		output = f.read()
		f.close
		errorDirPath = os.path.dirname(outputFile)
		dict['command']= command
		
		#check that dir or file exists
		resultDict=masDirExists (cssDir, errorDirPath)
		result=resultDict['retVal']
		dict['error'] = resultDict['error']
		dict['error2'] = resultDict['error2']
		dict['function2Command'] = resultDict['command']
		dict['retVal'] = resultDict['retVal']
		dict['result2'] = resultDict['result']
	
		#if it exists result will be 0 and while loop will exit
		#else count will increment and sleep will execute
		count = count + 1
		if (result == 1):
			masStoreDelay()
	return(dict)
	
def masFileExists ( cssFilePath, errorDirPath ):
	dict = {'function' : 'masDirFileExists'}
	#print "cssFilePath:  " + cssFilePath
	basePath = os.path.basename(cssFilePath) 
	errorFile = errorDirPath + "/fileMasLsError.txt"
	outputFile = errorDirPath + "/fileMasLsOutput.txt"
	if os.path.exists(errorFile):
		os.unlink(errorFile)
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -l1 " + cssFilePath + " 2> " + errorFile  + " > " + outputFile
	#print "command:  " + command
	dict['command']= command
	result=comWrap.comWrap (command)
	dict['result']= result
	dict['remoteFileSize']=0
	f = open(errorFile, 'r')
	error = f.read()
	f.close
	
	copyErrorStr="No such file or directory"
	errorCheck = errorFile.find(copyErrorStr)
	#print "errorCheck file ls:  " + str(errorCheck)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
		
	copyErrorStr="nodename nor servname provided, or not known"
	errorCheck = errorFile.find(copyErrorStr)
	#print "errorCheck nodename ls:  " +  str(errorCheck)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= "connection problem with MSS"
		dict['error2']= error.strip()
		return dict
	else:
		dict['retVal']= 0
		dict['error']= "none"
		dict['error2']="none"	
		#split on spaces 
		f = open(outputFile, 'r')
		firstLine = f.readline()
		#print "firstLine:  " + firstLine
		lineList = firstLine.split()
		#print "lineList:  " + str(lineList)
		if (len(lineList) > 4):
			remoteFileSize = int(lineList[3])
			dict['remoteFileSize']=remoteFileSize	
		f.close

		return dict
		
def masDirExists ( cssDir, errorDirPath ):
	dict = {'function' : 'masDirFileExists'}
	basePath = os.path.basename(cssDir) 
	errorFile = errorDirPath + "/fileMasLsError.txt"
	outputFile = errorDirPath + "/fileMasLsOutput.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -1d " + cssDir + " 2> " + errorFile  + " > " + outputFile
	#print "command:  " + command
	dict['command']= command
	result=comWrap.comWrap (command)
	dict['result']= result
	dict['remoteFileSize']=0
	f = open(errorFile, 'r')
	error = f.read()
	f.close
	
	copyErrorStr="No such file or directory"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
		
	copyErrorStr="nodename nor servname provided, or not known"
	errorCheck = errorFile.find(copyErrorStr)
	if errorCheck != -1:
		dict['retVal']= 1
		dict['error']= basePath + " does not exist"
		dict['error2']= error.strip()
		return dict
	else:
		dict['retVal']= 0
		dict['error']= "none"
		dict['error2']="none"	
		return dict

def masPutDelayTimeOut ( file, cssPath , errorFile, count=1 ):
	dict = {'function' : 'masPutDelayTimeOut'}
	dict['function2'] = 'masDirFileExists'
	dict['result2'] = ""
	dict['function2Command'] = "none"
	startTime = datetime.datetime.now()
	errorDirPath = os.path.dirname(errorFile)
	if os.path.exists(errorFile):
		os.unlink(errorFile)
	command = "/usr/local/bin/masput - "  + cssPath + " 2> " + errorFile + " < "+ file 
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	
	dict['command']= command
	
	count=1
	result=1
	oneSec=1

	#try to run command count times before giving up; result !=1 is successful execution
	while (count < 4 and result == 1):
		masStoreDelayCheck()
		commandResult=comWrap.timeout_command (command)
		
		#bash command timedOut
		if commandResult == None:
			result == 1
		#bash command excuted
		else:
			#check error file used in bash command
			f = open(errorFile, 'r')
			output = f.read()
			f.close
			copyErrorStr="No such file or directory"
			errorCheck = output.find(copyErrorStr)	
			if errorCheck == -1:
				#could not find "No such file or directory" error
				#masput produced no error
			
				#check if remote file exists
				resultDict=masFileExists (cssPath, errorDirPath)
			
				dict['error'] = resultDict['error'] + " - file exist error"
				dict['function2Command'] = resultDict['command']
				remoteFileSize = resultDict['remoteFileSize']
				localFileSize=os.path.getsize(file)
				if (remoteFileSize == localFileSize):
					#sizes of remote and local files are equal
					dict['retVal'] = resultDict['retVal']
					dict['result2'] = resultDict['result']
					result=0
				else:
					#sizes of remote and local files are not equal
					result=1
					dict['retVal']=1				
					dict['error'] = " remote file size: _" + str(remoteFileSize) + "_ does not equal local file size:  _" + str(localFileSize) + "_"
			else:
				#directory on MSS does not exist
				result=1
				dict['retVal']= 1
				dict['error']= copyErrorStr + " - masput error"
				cssDirName=os.path.dirname(cssPath)
				errorMasFileMkdir=errorDirPath + "/errorMasFileMkdir.txt"
				resultDict2=masMkdirDelay(cssDirName,errorMasFileMkdir)
				result=resultDict2['retVal']
				if result != 0:
					dict['function2'] = 'masMkdirDelay'
					dict['command'] = resultDict['command']
					dict['error']= resultDict['error2']
				waitTime=oneSec	
					
		count = count + 1
		if (result == 1):
			masStoreDelay()				
	endTime = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (endTime, startTime)
	dict['runTotalSeconds'] = timeDict['seconds']
	dict['runHours'] = timeDict['printHours']
	dict['runMins'] = timeDict['printMins']			
	dict['result']= result
	return(dict)
