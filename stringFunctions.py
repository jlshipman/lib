#!/usr/bin/python
import funcReturn

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def phone_format(n): 
	tel = format(int(n[:-1]), ",").replace(",", "-") + n[-1] 
	return tel
	
def strFind (stack, needle):
	retObj = funcReturn.funcReturn('strFind')
	val = stack.find(needle)
	retObj.setResult(val)
	if val > 0:
		retObj.setResult(val)
		retObj.setRetVal(0)
		retObj.setComment("found needle in string")
	return retObj
	
def isInt(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
        
def tabs (n):
	tab = "\t"
	result = ""
	for i in range(0, n):
		result = result + tab
	return result