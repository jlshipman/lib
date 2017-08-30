import subprocess, os, sys
import optparse
sys.path.append('lib')
from commandwrapper import *
import string
from fileFunctions import *
from listFunctions import *
import timeFunc
import datetime 
import time
import signal
import funcReturn


def comWrapMvSudo(src, dst):
	retObj = funcReturn.funcReturn('comWrapMvSudo')
	src = src.strip()
	dst = dst.strip()
	comWrapCommand='sudo mv ' + src + ' ' + dst
	retObj.setCommand(comWrapCommand)
	
	if not (os.path.exists (src)):
		error= "source file: "  + src + " does not exist"
		retObj.setError(error)
		return retObj
		
	command = comWrap (comWrapCommand)
	comment= os.path.exists ( dst )
	retObj.setComment(comment)
	#print (dict['test'])
	if (os.path.exists ( dst )):
		retObj.setRetVal(0)
	else:
		error= "destination file: "  + dst + " does not exist"
		retObj.setError(error)
	return retObj

def comWrapMv2(src, dst):
	retObj = funcReturn.funcReturn('comWrapMv2')
	src = src.strip()
	dst = dst.strip()
	comWrapCommand='mv ' + src + ' ' + dst
	retObj.setCommand(comWrapCommand)
	
	if not (os.path.exists (src)):
		error= "source file: "  + src + " does not exist"
		retObj.setError(error)
		return retObj
		
	command = comWrap (comWrapCommand)
	comment= os.path.exists ( dst )
	retObj.setComment(comment)
	#print (dict['test'])
	if (os.path.exists ( dst )):
		retObj.setRetVal(0)
	else:
		error= "destination file: "  + dst + " does not exist"
		retObj.setError(error)
	return retObj
	
def catFile ( filepath ):
	retObj = funcReturn.funcReturn('catFile')
	if (os.path.exists ( filepath )):
		comWrapCommand="/bin/cat " + filepath 
		retObj.setCommand(comWrapCommand)
		retObjCommand = comWrapString(comWrapCommand)
		retVal = retObjCommand.getRetVal()
		
		if retVal == 0:
			stdOut = retObjCommand.getStdout()
			retObj.setStdout(stdOut)
			retObj.setRetVal(0)
		else:
			error= "comWrapString: " + comWrapCommand
			retObj.setError(error)
	else:
		error= filepath + " does not exist"
		retObj.setError(error)
		
	return retObj

def checkSum ( fileCheckSum ):
	retObj = funcReturn.funcReturn('comWrapConvertTiff2Jpg')
	if (os.path.exists ( fileCheckSum )):
		comWrapCommand="/usr/bin/sum " + fileCheckSum 
		retObj.setCommand(comWrapCommand)
		retObjCommand = comWrapString(comWrapCommand)
		retVal = retObjCommand.getRetVal()
		
		if retVal == 0:
			stdOut = retObjCommand.getStdout()
			retObj.setStdout(stdOut)
			retObj.setRetVal(0)
		else:
			error= "comWrapString: " + comWrapCommand
			retObj.setError(error)
	else:
		error= fileCheckSum + " does not exist"
		retObj.setError(error)
		
	return retObj
	
#convert tiff files to jpg
def comWrapConvertTiff2JpgObj( tiffIn, jpgOut, size=1000):
	retObj = funcReturn.funcReturn('comWrapConvertTiff2Jpg')
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize ' + str(size) + 'x' + str(size) + ' -background white -gravity center -extent ' + str(size) + 'x' + str(size) + ' ' + jpgOut
		retObj.setCommand(comWrapCommand)
		command = comWrap (comWrapCommand)
		if (os.path.exists ( jpgOut )):
			retObj.setRetVal(0)
			return retObj
		else:
			error = jpgOut + " does not exist"
			retObj.setError(error)
			return retObj
	else:
		error= tiffIn + " does not exist"
		retObj.setError(error)
		return retObj	
		
#convert tiff files to jpg thumbs
def comWrapConvertTiff2JpgThumbObj( tiffIn, jpgOut, size=100):
	retObj = funcReturn.funcReturn('comWrapConvertTiff2JpgThumbObj')
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize ' + str(size) + 'x' + str(size) + ' -background white -gravity center -extent ' + str(size) + 'x' + str(size) + ' ' + jpgOut
		retObj.setCommand(comWrapCommand)
		command = comWrap (comWrapCommand)
		if (os.path.exists ( jpgOut )):
			retObj.setRetVal(0)
			return retObj
		else:
			error = jpgOut + " does not exist"
			retObj.setError(error)
			return retObj
	else:
		error= tiffIn + " does not exist"
		retObj.setError(error)
		return retObj	
		
def which (command):
	#test to see if command is available
	commandStr = "which " + command
	retObj = comWrapString(commandStr)
	retObj.setCommand(commandStr)
	retObj.setName('which')
	
	return retObj
	
def timeout_command(command, timeout):
    ##call shell-command and either return its output or kill it
    ##if it is killed it will return None 

    cmd = command.split(" ")
    start = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while process.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            return None

    return process.stdout.read()
	
def comWrapRetObj(appleCommandList, super=False):
	#print "comWrapRetObj"
	retObj = funcReturn.funcReturn('comWrapRetObj')
	if super == True:
		appleCommandList.insert(0, "sudo")
	commandStr = ' '.join(appleCommandList)
	#print commandStr
	#print "appleCommandList:  " + str(appleCommandList)
	process = subprocess.Popen(appleCommandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	
 	retObj.setCommand(commandStr)
 	#print "stdout:  " + stdout
 	#print "stderr:  " + stderr
	retObj.setStderr(stderr.strip())
	retObj.setStdout(stdout.strip())
	rc = process.returncode
 	#print "rc:  " + str(rc)
	retObj.setRetVal(rc)
	return retObj

def comWrapString(cmdString,cwd=None):
	retObj = funcReturn.funcReturn('comWrapString')
	#print(cmdString)
	process = subprocess.Popen(cmdString, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
 	#print "cmdString:  " + str(cmdString)
 	#print "stdout:  " + stdout
 	#print "stderr:  " + stderr
	retObj.setStderr(stderr.strip())
	retObj.setStdout(stdout.strip())
	rc = process.returncode
	retObj.setCommand(cmdString)
 	#print "rc:  " + str(rc)
	retObj.setRetVal(rc)
	return retObj
	  	
def comWrap2(appleCommandList):
	dict = {'function' : 'comWrap2'}
	dict['retVal'] = 0
	dict['error'] = ""
	dict['stdout'] = ""
	dict['stderr'] = ""
	dict['comment'] = ""
	dict['result'] = ""
	dict['command'] = ""
	process = subprocess.Popen(appleCommandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = process.communicate()
	dict['stderr'] = stderr
	dict['stdout'] = stdout
	return dict
		     
def comWrap(cmd,cwd=None):
	 '''runs a command in the comWrap shell'''
	 #print(cmd)
	 retVal = subprocess.Popen(cmd, shell=True, \
		  stdout=subprocess.PIPE, cwd=cwd).stdout.read().strip('\n').split('\n')
	 if retVal==['']:
		  return(0)
	 else:
		  return(retVal)

def comWrapTarMasput (item2Tar, cssArchive, tarErrorFile):
	dict = {'function' : 'comWrapTarMasput'}
	if os.path.exists(tarErrorFile):
		os.unlink(tarErrorFile)
	errorDirPath = os.path.dirname(tarErrorFile)
	massPutErrorFile = errorDirPath + "/masPutErrorFile.txt"
	if os.path.exists(massPutErrorFile):
		os.unlink(massPutErrorFile)
	#command='/usr/bin/tar -cf - ' + item2Tar + ' 2> ' + tarErrorFile + ' | gzip -1 | /usr/local/bin/masput - ' + cssArchive + ' 2> ' + massPutErrorFile
	command='/usr/bin/tar -cf - ' + item2Tar + ' 2> ' + tarErrorFile +  ' | /usr/local/bin/masput - ' + cssArchive + ' 2> ' + massPutErrorFile
	#print command
	result=comWrap (command)
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
		
	resultDict=comWrapMasDirFileexists (cssArchive, errorDirPath)
	dict['function2'] = 'comWrapMasDirFileexists'
	dict['error'] = resultDict['error']
	dict['error2'] = resultDict['error2']
	dict['function2Command'] = resultDict['command']
	dict['retVal'] = resultDict['retVal']
	dict['result2'] = resultDict['result']
	return(dict)
	
def checkForProcess(processName):
	dict = {'function' : 'checkForProcess'}
	comWrapCommand='ps -f|grep ' + processName	
	try:
		#perform a ps command and assign results to a list
		command = WrapCommand (comWrapCommand)
		result = command ()
		#print result
		proginfo = string.splitcommand
		#print proginfo
		dict['uid']= proginfo[0]
		dict['pid']= proginfo[1]
		dict['parent']= proginfo[2]
		dict['CPUusage']= proginfo[3]
		dict['timeStarted']= proginfo[4]
		dict['controllingTTY']= proginfo[5]
		dict['retVal']= 0
	except:
		dict['retVal']= 1
		dict['error']= "There was a problem with checkForProcess."
		
def comWrapMv(src, dst):
	dict = {'function' : 'comWrapMv'}
	src = src.strip()
	dst = dst.strip()
	comWrapCommand='mv ' + src + ' ' + dst
	dict['command']= comWrapCommand
	
	if not (os.path.exists (src)):
		dict['retVal']= 1
		dict['error']= "source file: "  + src + " does not exist"
		return dict
		
	command = comWrap (comWrapCommand)
	dict['test']= os.path.exists ( dst )
	#print ("_"+dst+"_")
	#print (dict['test'])
	if (os.path.exists ( dst )):
		dict['retVal']= 0
		dict['error']= "none"
		return dict
	else:
		dict['retVal']= 1
		dict['error']= "destination file: "  + dst + " does not exist"
		return dict
		
def comWrapSSH(src, connect, dst, user, outputFile):
	dict = {'function' : 'comWrapSSH'}
	scpCommand="/usr/bin/scp " + src + " " + connect + ":" +dst
	comWrapCommand="/usr/bin/sudo -u " + user + " " + scpCommand + " 2> " + outputFile
	command = comWrap (comWrapCommand)
	
	f = open(outputFile, 'r')
	output = f.read()
	f.close
	copyErrorStr="Permission denied"
	errorCheck = output.find(copyErrorStr)
	if errorCheck == -1:
		dict['retVal']= 0
	else:
		dict['retVal']= 1
		
	dict['command']= comWrapCommand
	dict['output']= output
	dict['errorCheck']= errorCheck
	return (dict)
	
#convert tiff files to jpg
def comWrapConvertTiff2Jpg( tiffIn, jpgOut):
	dict = {'function' : 'comWrapConvertTiff2Jpg'}
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize 500x500 -background white -gravity center -extent 500x500 ' + jpgOut
		dict['command']= comWrapCommand
		command = comWrap (comWrapCommand)
		dict['test']= os.path.exists ( jpgOut )
		if (os.path.exists ( jpgOut )):
			dict['retVal']= 0
			dict['error']= "none"
			return dict
		else:
			dict['retVal']= 1
			dict['error']= jpgOut + " does not exist"
			return dict
	else:
		dict['retVal']= 1
		dict['error']= tiffIn + " does not exist"
		return dict		
		
#convert tiff files to jpg thumbs
def comWrapConvertTiff2JpgThumb( tiffIn, jpgOut):
	dict = {'function' : 'comWrapConvertTiff2JpgThumb'}
	dict['command']=""
	dict['error']=""
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize 72x72 -background white -gravity center -extent 72x72 ' + jpgOut
		dict['command']= comWrapCommand
		command = comWrap (comWrapCommand)
		dict['test']= os.path.exists ( jpgOut )
		if (os.path.exists ( jpgOut )):
			dict['retVal']= 0
			dict['error']= "none"
			return dict
		else:
			dict['retVal']= 1
			dict['error']= jpgOut + " does not exist"
			return dict
	else:
		dict['retVal']= 1
		dict['error']= tiffIn + " does not exist"
		return dict		
			
#unlock files
def comWrapUnlock ( fileDir ):
	command = '/usr/bin/chflags -R nouchg ' + fileDir
	retVal = comWrap (command)
	return retVal
	
#delete file or directory
def comWrapDelete ( file ):
	comWrapCommand = '/bin/rm -rf ' + file
	command = WrapCommand (comWrapCommand)
	result = command ()
	if not (os.path.exists ( file )):
		return(0)
	else:
		return(1)
	
def comWrapMasTapeCheck (archive):
	 masCommand = '/usr/local/bin/masls -alm  ' + archive
	 command = WrapCommand (masCommand)
	 result = command ()
	 firstChar = result[0]
	 #where "-" is file on disk cache only, 
	 #"m" is file on disk cache and on tape, 
	 #and "M" is file on tape only. 
	 return firstChar
 
def comWrapMasls (archive):
	 masCommand = '/usr/local/bin/masls -1  ' + archive
	 command = WrapCommand (masCommand)
	 result = command ()
	 return result
	 		
def comWrapCSSfileSize (file):
	#cssBytes=`/usr/local/bin/masls -al  "$dmss_split" | awk '{print $4}'`
	command = "/usr/local/bin/masls -al " + file + " | awk '{print $4}' "
	retVal=comWrap (command)
	if retVal[0]==['']:
		return(0)
	else:
		return(retVal[0])
	
def comWrapCheckSum ( fileCheckSum, fileOutput ):
	command = "/usr/bin/sum " + fileCheckSum + " > " + fileOutput
	result=comWrap (command)
	return(result)
	
def countLinesInFile ( file ):
	non_blank_count = 0

	with open(file) as infp:
		for line in infp:
			if line.strip():
			  non_blank_count += 1
	return non_blank_count

def comWrapStdOutNone(cmd,cwd=None):
	 '''runs a command in the comWrap shell'''
	 #print(cmd)
	 retVal = subprocess.Popen(cmd, shell=True, \
		  stdin=None, stdout=None, stderr=None)
	 if retVal==['']:
		  return(0)
	 else:
		  return(retVal)
		  			  
def comWrapSplit ( Amount, pathArchive, pathSplit ):
	#split -a 3 -b $splitAmount ${tempTar}$tarFile "${tempSplit}$tarFile.part-"
	command = "/usr/bin/split -a 3 -b " + Amount + " " + pathArchive + " " + pathSplit
	result=comWrap (command)
	return(result)

def comWrapTar2 ( pathArchive, localDir, tarErrorFile ):
	dict = {'function' : 'comWrapTar2'}
	startTime = datetime.datetime.now()
	curDir=os.getcwd()
	#gnutar -cvf  $tempTar$tarFile "$local_dir"
	base=os.path.basename(localDir)
	dirName=os.path.dirname(localDir)
	os.chdir(dirName)
	command = "/usr/bin/tar -cf " + pathArchive + " " + base + " 2> " + tarErrorFile
	dict['command']= command
	result=comWrap (command)
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
		
def comWrapTar ( pathArchive, localDir ):
	#gnutar -cvf  $tempTar$tarFile "$local_dir"
	command = "/usr/bin/gnutar -cf " + pathArchive + " " + localDir
	result=comWrap (command)
	return(result)
	
def comWrapMasmkdir ( cssDir, outputFile ):
	dict = {'function' : 'comWrapMasmkdir'}
	command = "/usr/local/bin/masmkdir -p " + cssDir + " 2> " + outputFile
	errorDirPath = os.path.dirname(outputFile)
	dict['command']= command
	result=comWrap (command)
	resultDict=comWrapMasDirExists (cssDir, errorDirPath)
	dict['function2'] = 'comWrapMasDirFileexists'
	dict['error'] = resultDict['error']
	dict['error2'] = resultDict['error2']
	dict['function2Command'] = resultDict['command']
	dict['retVal'] = resultDict['retVal']
	dict['result2'] = resultDict['result']
	return(dict)

def comWrapMasDirFileexists ( cssDir, errorDirPath ):
	dict = {'function' : 'comWrapMasDirFileexists'}
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
	result=comWrap (command)
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
			
def comWrapMasDirListing ( cssDir, errorDirPath ):
	dict = {'function' : 'comWrapMasDirListing'}
	cssDir = cssDir.rstrip("/")
	errorFile = errorDirPath + "/errorDirMasLs.txt"
	outputFile = errorDirPath + "/outputDirMasLs.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -1 " + cssDir + "/" + " 2> " + errorFile + "  > " + outputFile 
	dict['command']= command
	result=comWrap (command)
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
		listDirContents = listFromFile(outputFile)
		dict['listDirContents']=listDirContents
		return dict
				
def comWrapMasput ( file, cssPath , errorFile ):
	dict = {'function' : 'comWrapMasput'}
	errorDirPath = os.path.dirname(errorFile)
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput " + file + " " + cssPath + " 2> " + errorFile
	dict['command']= command
	#print command
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	#print "cssSplitPath:  " + cssSplitPath
	#print "command:  " + command
	result=comWrap (command)
	f = open(errorFile, 'r')
	output = f.read()
	f.close
	copyErrorStr="No such file or directory"
	errorCheck = output.find(copyErrorStr)
	if errorCheck == -1:
		dict['retVal']= 0
		dict['result']= result
		resultDict=comWrapMasDirFileexists (cssSplitPath, errorDirPath)
		dict['function2'] = 'comWrapMasDirFileexists'
		dict['error'] = resultDict['error'] + " - file exist error"
		dict['function2Command'] = resultDict['command']
		dict['retVal'] = resultDict['retVal']
		dict['result2'] = resultDict['result']
	else:
		dict['retVal']= 1
		dict['error']= copyErrorStr + " - masput error"
	return(dict)

def comWrapMasputDelay ( file, cssPath , errorFile ):
	dict = {'function' : 'comWrapMasputDelay'}
	dict['function2'] = 'comWrapMasDirFileexists'
	startTime = datetime.datetime.now()
	errorDirPath = os.path.dirname(errorFile)
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput " + file + " " + cssPath + " 2> " + errorFile
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	
	dict['command']= command
	
	count=1
	result=1
	minute = 60 #seconds
	fiveMin = minute * 5
	hour = 60 * minute
	
	while (count < 4 and result == 1):
		result=comWrap (command)
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
			resultDict=comWrapMasDirFileexists (cssSplitPath, errorDirPath)
			dict['function2'] = 'comWrapMasDirFileexists'
			dict['error'] = resultDict['error'] + " - file exist error"
			dict['function2Command'] = resultDict['command']
			dict['retVal'] = resultDict['retVal']
			dict['result2'] = resultDict['result']
		else:
			dict['retVal']= 1
			dict['result']= 1
			dict['error']= copyErrorStr + " - masput error"
			
		count = count + 1
		numWeekDay=datetime.datetime.today().weekday()
		if (result == 1):
			if not (numWeekDay == 1 ) :				
				time.sleep (fiveMin)
			else:
				now = datetime.datetime.now()
				hoursTilWed = now.hour - 24
				hourDelay = hoursTilWed + 6
				secDelay = hour * hourDelay
				time.sleep (secDelay)			

	return(dict)
	
def comWrapMasputDelay2 ( file, cssPath , errorFile ):
	dict = {'function' : 'comWrapMasputDelay'}
	dict['function2'] = 'comWrapMasDirFileexists'
	startTime = datetime.datetime.now()
	errorDirPath = os.path.dirname(errorFile)
	#/usr/local/bin/masput $tempSplit$splitTar  "$dmss_split" 2>${baseTemp}stderr
	command = "/usr/local/bin/masput - "  + cssPath + " 2> " + errorFile + " < "+ file 
	basePath = os.path.basename(file) 
	cssSplitPath = cssPath + "/" + basePath
	dict['function2Command'] = ""
	dict['command']= command
	
	count=1
	result=1
	oneSec=1
	minute = 60 #seconds
	fiveMin = minute * 5
	hour = 60 * minute
	waitTime=fiveMin
	while (count < 4 and result == 1):
		result=comWrap (command)
		f = open(errorFile, 'r')
		output = f.read()
		f.close
		copyErrorStr="No such file or directory"
		errorCheck = output.find(copyErrorStr)	
		if errorCheck == -1:
			#masput produced no error
			
			#check if remote file exists
			resultDict=comWrapMasFileExists (cssPath, errorDirPath)
			
			dict['error'] = resultDict['error'] + " - file exist error"
			dict['function2Command'] = resultDict['command']
			commentRemote = "remoteFileSize:  " + str(resultDict['remoteFileSize']) 
			remoteFileSize = resultDict['remoteFileSize']
			localFileSize=os.path.getsize(file)
			#localFileSize = fileSize(file)
			commentLocal = "localFileSize:   " + str(localFileSize)
			commentList = [commentRemote, commentLocal]
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
				waitTime=fiveMin
		else:
			#directory on MSS does not exist
			result=1
			dict['retVal']= 1
			dict['error']= copyErrorStr + " - masput error"
			cssDirName=os.path.dirname(cssPath)
			errorMasFileMkdir=errorDirPath  + "/errorMasFileMkdir.txt"
			resultDict2=comWrapMasmkdirDelay(cssDirName,errorMasFileMkdir)
			result=resultDict2['retVal']
			if result != 0:
				dict['function2'] = 'comWrapMasmkdirDelay'
				dict['command'] = resultDict['command']
				dict['error']= resultDict['error2']
			waitTime=oneSec	
			
		count = count + 1
		numWeekDay=datetime.datetime.today().weekday()
		if (result == 1):
			if not (numWeekDay == 1 ) :			
				time.sleep (waitTime)
			else:
				now = datetime.datetime.now()
				hoursTilWed = now.hour - 24
				hourDelay = hoursTilWed + 6
				secDelay = hour * hourDelay
				time.sleep (secDelay)
				
	endTime = datetime.datetime.now()
	timeDict = timeFunc.timeDuration2 (endTime, startTime)
	dict['runTotalSeconds'] = timeDict['seconds']
	dict['runHours'] = timeDict['printHours']
	dict['runMins'] = timeDict['printMins']			
	dict['result']= result
	dict['comment'] = commentList
	return(dict)
	
def comWrapMasmkdirDelay ( cssDir, outputFile ):
	dict = {'function' : 'comWrapMasmkdir'}
	command = "/usr/local/bin/masmkdir -p " + cssDir + " 2> " + outputFile
	
	count=1
	result=1
	minute = 60 #seconds
	fiveMin = minute * 5
	hour = 60 * minute
	
	while (count < 4 and result == 1):
		#currently errorFile is not check neither is
		#result at this point
		result=comWrap (command)
		print "result:  " + str(result)
		dict['result']=result
		
		f = open(outputFile, 'r')
		output = f.read()
		f.close
		errorDirPath = os.path.dirname(outputFile)
		dict['command']= command
		
		#check that dir or file exists
		resultDict=comWrapMasDirExists (cssDir, errorDirPath)
		result=resultDict['retVal']
		
		dict['function2'] = 'comWrapMasDirFileexists'
		dict['error'] = resultDict['error']
		dict['error2'] = resultDict['error2']
		dict['function2Command'] = resultDict['command']
		dict['retVal'] = resultDict['retVal']
		dict['result2'] = resultDict['result']
	
		#if it exists result will be 0 and while loop will exit
		#else count will increment and sleep will execute
		count = count + 1
		numWeekDay=datetime.datetime.today().weekday()
		if (result == 1):
			if not (numWeekDay == 1 ) :				
				time.sleep (fiveMin)
			else:
				now = datetime.datetime.now()
				hoursTilWed = now.hour - 24
				hourDelay = hoursTilWed + 6
				secDelay = hour * hourDelay
				time.sleep (secDelay)	

	return(dict)
	
def comWrapMasFileExists ( cssFilePath, errorDirPath ):
	dict = {'function' : 'comWrapMasDirFileexists'}
	#print "cssFilePath:  " + cssFilePath
	basePath = os.path.basename(cssFilePath) 
	errorFile = errorDirPath + "/fileMasLsError.txt"
	outputFile = errorDirPath + "/fileMasLsOutput.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -l1 " + cssFilePath + " 2> " + errorFile  + " > " + outputFile
	#print "command:  " + command
	dict['command']= command
	result=comWrap (command)
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
		
def comWrapMasDirExists ( cssDir, errorDirPath ):
	dict = {'function' : 'comWrapMasDirFileexists'}
	basePath = os.path.basename(cssDir) 
	errorFile = errorDirPath + "/fileMasLsError.txt"
	outputFile = errorDirPath + "/fileMasLsOutput.txt"
	if os.path.exists(outputFile):
		os.unlink(outputFile)
	command = "/usr/local/bin/masls -1d " + cssDir + " 2> " + errorFile  + " > " + outputFile
	#print "command:  " + command
	dict['command']= command
	result=comWrap (command)
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
