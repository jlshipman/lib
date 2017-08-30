#!/usr/bin/python
try:
	import mysql.connector
	import csv
	import funcReturn
except ImportError:
	print "missing modules for mysqlFunctions.py"
	sys.exit(1)

def connection (hostName, userName, passwd, databaseName):
	conn = mysql.connector.Connect(host=hostName,user=userName,\
                        password=passwd,database=databaseName)
	return conn

def exportCSV (data, exportFile):
	retObj = funcReturn.funcReturn('exportCSV')
	#print "data:  " + str(data)
	#print "exportFile:  " + str(exportFile)
	whole = ""
	try:
		f = open(exportFile, "w")
		for row in data:
			line = str(row)
			line = line.strip('"')
			line = line.lstrip('(')
			line = line.rstrip(')')
			whole = whole + line + "\n"
			
		whole = whole.rstrip('\n')
		f.write(whole)
		retObj.setRetVal(0)
	except Exception:
			retObj.setError("problem exporting records")
	return retObj	
	
def showQuery ( query, stringArray, searchArray):
	#print "query"
	retObj = funcReturn.funcReturn('showQuery')
	lenStringArray = len(stringArray)
	lenSearchArray = len(searchArray)
	if lenStringArray != lenSearchArray:
		retObj.setError("Arrays are unequal in length")
		return retObj
	
	end = lenStringArray
# 	print "stringArray:  " + str(stringArray)
# 	print "searchArray:  " + str(searchArray)
# 	print "lenSearchArray:  " + str(lenSearchArray)
	
	for n in range(0, end):
		try:
				old = str(stringArray[n])
				new = '"' + str(searchArray[n]) + '"'
				#print "old:  " + str(old)
				#print "new:  " + str(new)
				query = query.replace(old, new, 1)
		except Exception:
				retObj.setError("problem showQuery - " + str(new))
				return retObj
	
	#print 	"query:  " + query
	retObj.setRetVal(0)
	retObj.setResult(query)
	return retObj	