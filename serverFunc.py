import listFunctions
import remoteFunc
import subprocess

def servers(serverListFile, processListFile, outputLogFile, outputLogFile2, stage, func):
	dict = {'function' : 'servers'}
	sep=","
	dict['retVal'] = 0
	dict['error'] = ""
	dict['comment'] = "\n"
	serverList=listFunctions.listFromFile(serverListFile)
	for line in serverList:
		hostname, user, localRemote= line.split(sep);
		string=hostname + "  " + str(user) + "  " + str(localRemote)
		dict['comment'] = dict['comment'] +  "   " + string + "\n"
		retDict = func (hostname, user, processListFile, localRemote, stage, outputLogFile, outputLogFile2)
		dict['retVal'] = dict['retVal'] + retDict['retVal']
		dict['error'] = dict['error'] + retDict['error']
		dict['comment'] = dict['comment'] + retDict['comment']
	return dict
	
def processGrepSpawn (hostname, user, processListFile, localRemote, stage, outputLogFile, outputLogFile2):
	dict = {'function' : 'servers'}	
	dict['retVal'] = 0
	dict['error'] = ""
	dict['comment'] = ""
	processList=listFunctions.listFromFile(processListFile)
	sep=","
	for p in processList:
		dict['comment'] = dict['comment'] +  "      " + p + "\n"
		found = 0
		code, searchItem, restart= p.split(sep)
		localCode, localParam=code.split()
		if localRemote.strip() == "remote":
			resultDict=remoteFunc.runCodeRemoteUnix(hostname, user, code, stage, outputLogFile )
			if int(resultDict['retVal']) == 0:
				outputList=listFunctions.stringToList(str(resultDict['output']), "\n")
				for item in outputList:
					if item.find(searchItem) != -1:
						dict['comment'] = dict['comment'] + "        found:  " + item + "\n"
						found = 1
				if found == 0 and restart != "none":
					resultDict=remoteFunc.runCodeRemoteUnix(hostname, user, restart, stage, outputLogFile2)
				#l.info( "   " + str(resultDict['output']))
			else:
				dict['error'] = dict['error'] + "        error: " + str(resultDict['error']) + "\n"
				dict['retVal'] = dict['retVal'] + 1 
		else:
			try:
				output=subprocess.check_output([localCode, localParam])
				outputList=listFunctions.stringToList(str(output), "\n")
				for item in outputList:
					if item.find(searchItem) != -1:
						found = 1
				if found == 0 and restart != "none":
					dict['comment'] = dict['comment'] + "        found none:  " + restart + "\n"
					localCode, localParam= restart.split(" ")
					output=subprocess.check_output([localCode, localParam])			
			except subprocess.CalledProcessError, e:
				dict['error'] = dict['error'] + "   error: " + code + "  :  " + e.output
				dict['retVal'] = dict['retVal'] + 1 
	return dict
	
def processSpawn (hostname, user, processListFile, localRemote, stage, outputLogFile, outputLogFile2):
	dict = {'function' : 'servers'}	
	dict['retVal'] = 0
	dict['error'] = ""
	dict['comment'] = ""
	processList=listFunctions.listFromFile(processListFile)
	sep=","
	for p in processList:
		dict['comment'] = dict['comment'] +  "      " + p + "\n"
		found = 0
		code = p
		print code
		localCode, localParam=code.split(" ", 1)
		print localCode
		print localParam
		if localRemote.strip() == "remote":
			resultDict=remoteFunc.runCodeRemoteUnix(hostname, user, code, stage, outputLogFile )
			if int(resultDict['retVal']) == 0:
				outputList=listFunctions.stringToList(str(resultDict['output']), "\n")
			else:
				dict['error'] = dict['error'] + "        error: " + str(resultDict['error']) + "\n"
				dict['retVal'] = dict['retVal'] + 1 
		else:
			try:
				output=subprocess.check_output([localCode, localParam])
				outputList=listFunctions.stringToList(str(output), "\n")
			except subprocess.CalledProcessError, e:
				dict['error'] = dict['error'] + "   error: " + code + "  :  " + e.output
				dict['retVal'] = dict['retVal'] + 1 
	return dict