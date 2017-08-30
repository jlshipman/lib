#!/usr/bin/python
from collections import OrderedDict
import funcReturn

def dictToFile2(dict, filePath, sep):
	retObj = funcReturn.funcReturn('dictToFile2')
	return retObj
	
	
def fileToDict( filePath, sep ):
	resDict = {}
	with open(filePath,"r") as text:
		for line in text:
			key, value = line.split(sep)
			resDict[key] = str(value.strip())
	return resDict

#create dict from file with substitution	
def fileToDictSub( filePath, sep ):
	resDict = {}
	with open(filePath,"r") as text:
		for line in text:
			list = line.split(sep)
			count = len(list)
			if count == 2:
				key, value = line.split(sep)
				resDict[key.strip()] = str(value.strip())
			elif count == 3:
				#search dict for value to add to value created now
				key, sub, value = line.split(sep)
				addVal = resDict[sub.strip()]
				resDict[key.strip()] = addVal + str(value.strip())
	return resDict
	
def dictToFile(dict, filePath, sep):
	resDict = {'function' : 'dictToFile'}
	resDict['retVal'] = 0
	file = open(filePath, 'w')
	ordDict = OrderedDict(sorted(dict.items(), key=lambda t: t[0]))
	for key, value in ordDict.items():
		string=key + sep + str(value) + "\n"
		file.write(string)
	file.close()
	return resDict