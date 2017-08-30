import math

class file_Size(object):
    """
    Container for a size in bytes with a human readable representation
    Use it like this::

        >>> size = fileSize(123123123)
        >>> print size
        '117.4 MB'
    """

    chunk = 1024
    units = ['bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    precisions = [0, 0, 1, 2, 2, 2]



    def __init__(self, size):
		self.size = size
		if size == 0:
			unit = 'bytes'
		else:
			unit = self.units[min(int(math.log(self.size, self.chunk)), len(self.units) - 1)]
		self.unit = unit
		exponent = self.units.index(unit)
		quotient = round((float(self.size) / self.chunk**exponent), 2)
		self.quotient = quotient

    def getSize(self):
    	return self.size
    	 	   
    def format(self, unit):
        if unit not in self.units: 
        	raise Exception("Not a valid file size unit: %s" % unit)
        if self.size == 1 and unit == 'bytes': 
        	return '1 byte'
        exponent = self.units.index(unit)
        quotient = round((float(self.size) / self.chunk**exponent), 2)
        self.quotient = quotient
        result = str(quotient) + " " + unit
        return result
     

    def getMB(self):
    	unitIndex = self.units.index(self.unit)
    	indexMove = unitIndex - 2
    	if indexMove > 0:
    		result = self.quotient * self.chunk**indexMove
    	if indexMove < 0:
    		result = self.quotient / self.chunk**math.fabs(indexMove)
    	if indexMove == 0:
    		result = self.quotient
    	return result
 
    def getGB(self):
    	unitIndex = self.units.index(self.unit)
    	indexMove = unitIndex - 3
    	if indexMove > 0:
    		result = self.quotient * self.chunk**indexMove
    	if indexMove < 0:
    		result = self.quotient / self.chunk**math.fabs(indexMove)
    	if indexMove == 0:
    		result = self.quotient
    	return result
    	    		   
    def getUnit(self):
    	return self.unit
    	
    def getQuotient(self):
    	return self.quotient
    			