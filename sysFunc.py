import subprocess, os, sys
import optparse
from subprocess import call
sys.path.append('lib')
import commandwrapper
import string
import fileFunctions
import listFunctions
import timeFunc
import datetime 
import time


	
def checkForProcess(processName):
	dict = {'function' : 'checkForProcess'}
	comWrapCommand='ps -f|grep ' + processName	
	try:
		#perform a ps command and assign results to a list
		command = commandwrapper.WrapCommand (comWrapCommand)
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
		
def SSHfunc(src, connect, dst, user, outputFile):
	dict = {'function' : 'SSHfunc'}
	scpCommand="/usr/bin/scp " + src + " " + connect + ":" +dst
	comWrapCommand="/usr/bin/sudo -u " + user + " " + scpCommand + " 2> " + outputFile
	command = commandwrapper.comWrap (comWrapCommand)
	
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
			
#unlock files
def unlockFiles ( fileDir ):
	command = '/usr/bin/chflags -R nouchg ' + fileDir
	retVal = commandwrapper.comWrap (command)
	return retVal
	
#delete file or directory
def deleteFileDir ( file ):
	comWrapCommand = '/bin/rm -rf ' + file
	command = commandwrapper.WrapCommand (comWrapCommand)
	result = command ()
	if not (os.path.exists ( file )):
		return(0)
	else:
		return(1)
	
def checkSumFunc ( fileCheckSum, fileOutput ):
	command = "/usr/bin/sum " + fileCheckSum + " > " + fileOutput
	result= commandwrapper.comWrap (command)
	return(result)
	
def mvFunc(src, dst):
	dict = {'function' : 'comWrapMv'}
	comWrapCommand='mv ' + src + ' ' + dst
	dict['command']= comWrapCommand
	
	if not (os.path.exists (src)):
		dict['retVal']= 1
		dict['error']= "souce file: "  + src + " does not exist"
		return dict
		
	command = commandwrapper.comWrap (comWrapCommand)
	dict['test']= os.path.exists ( dst )
	if (os.path.exists ( dst )):
		dict['retVal']= 0
		dict['error']= "none"
		return dict
	else:
		dict['retVal']= 1
		dict['error']= "destination file: "  + dst + " does not exist"
		return dict
