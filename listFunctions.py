#!/usr/bin/python
from collections import OrderedDict
from sets import Set
import funcReturn

def noDuplicates (theList):
	return list(OrderedDict.fromkeys(theList))

# given a list of lists where you wish not to have duplicates from the particular index	
def noDuplicatesListofList(theList, index):
	seen = Set()
	newList = []
	for l in theList:
		if l[index] not in seen :
			newList.append(l)
			seen.add(l[index])
	return newList
	
def removeValuesList(theList, value):
	while value in theList:
		theList.remove(value)

def listofListFromFile (filePath, sep):
	f = open(filePath)
	list = []
	lines = f.readlines()
	for line in lines:
		list.append(line.rstrip().split(sep))
	f.close()
	return list

def listFromFile (filePath):
	f = open(filePath)
	list = []
	lines = f.readlines()
	for line in lines:
		list.append(line.rstrip())
	f.close()
	return list
	
def listToString(theList, sep = " "):
	theString =sep.join(str(item) for item in theList)
	return theString

def stringToList(theString, sep = None):
	if (sep == None):
		theList=theString.split()
	else:
		theList=theString.split(sep)
	return theList
	
#create list of found and not found list based on the values in
#the first list existing in the second
def listComp(list1, list2):
	dict = {'function' : 'listComp'}
	foundList = []
	notFoundList = []
	for val in list1:
		if val in list2:
			foundList.append(val)
		else:
			notFoundList.append(val) 	
	dict['foundList'] = foundList
	dict['notFoundList'] = notFoundList
	return dict

#create list of found and not found list based on the values in
#the first list existing in the second list index
def listLolComp(list, lol, index):
	dict = {'function' : 'listLolComp'}
	foundList = []
	notFoundList = []
	for val in list:
		found = 0
		for l in lol:
			if l[index] == val:
				found = 1
				
		if found == 1:
			foundList.append(val)
		else:
			notFoundList.append(val) 	
	dict['foundList'] = foundList
	dict['notFoundList'] = notFoundList
	return dict

#create list of found and not found list based on the values in
#the first list of list index existing in the second list 
def lolListlComp(lol, index, list, sep):
	print "lolListlComp"
	dict = {'function' : 'lolListlComp'}
	foundList = []
	notFoundList = []
	for l in lol:
		#print "\tl:  " + str(l)
		found = 0
		val = l[index]
		for x in list:
			if x == val:
				found = 1
				
		if found == 1:
			#print "\t\tfound val:  " + str(val)
			foundList.append(val)
		else:
			#print "\t\tnot found l:  " + sep.join(l)
			notFoundList.append(l) 	
	dict['foundList'] = foundList
	dict['notFoundList'] = notFoundList
	return dict

#create list of found and not found list based on the values in
#the first list of list index existing in the second list 
def lolLolComp2(lol, index, lol2, index2):
	retObj = funcReturn.funcReturn('lolLolComp2')
	notFoundList = []
	for l in lol:
		found = 0
		val = l[index]
		for l2 in lol2:
			val2 = l2[index2]
			if val2 == val:
				found = 1
				
		if found == 0:
			notFoundList.append(l) 
	
	retObj.setResult(notFoundList)
	
	return retObj

#create list of found and not found list based on the values in
#the first list of list index existing in the second list 
def lolLolSetDiff(lol, index, lol2, index2):
	retObj = funcReturn.funcReturn('lolLolSetDiff')
	setOne = set()
	setTwo = set()
	for l in lol:
		setOne.add(l[index])
	for l in lol2:
		setTwo.add(l[index])
		
	#return set setOne after removing elements found in setTwo
	setDiff = setOne - setTwo 

	retObj.setResult(setDiff)
	
	return retObj
	
#create list of found and not found list based on the values in
#the first list of list index existing in the second list 
def lolLolComp(lol, index, lol2, index2):
	dict = {'function' : 'lolLolComp'}
	foundList = []
	notFoundList = []
	for l in lol:
		found = 0
		val = l[index]
		for l2 in lol2:
			val2 = l2[index2]
			if val2 == val:
				found = 1
				
		if found == 1:
			foundList.append(l2)
		else:
			notFoundList.append(l) 
	#found list: contains items from lol that exist in lol2	
	dict['foundList'] = foundList
	
	#notfound list: items from lol that do not exist in lol2	
	dict['notFoundList'] = notFoundList
	return dict
	
def listRemoveSubString(thelist, substring):
	thelist = [l.replace(substring, '').strip() for l in thelist]
	return thelist
	
def listofListRemoveSubString(theList, substring, Index):
	for l in theList:
		new=l[Index].replace(substring, '').strip()
		l[Index]=new
	return theList