import subprocess, os, sys
import optparse
from subprocess import call
sys.path.append('lib')
import comWrap
import string
import fileFunctions
import listFunctions
import timeFunc
import datetime 
import funcReturn
import time
import Image


def perserverAspectRation (xorig, yorig, newSize):
	retObj = funcReturn.funcReturn('perserverAspectRation')
	#print "xorig:  " + str(xorig)
	#print "yorig:  " + str(yorig)
	if (xorig >= yorig):
		xsize = newSize
		#print "x is greater"
		ratio = float(yorig) / float(xorig)
		#print "ratio:  " + str(ratio)
		ysize = int(ratio * xsize)
	else:
		ysize = newSize
		#print "y is greater"
		ratio = float(xorig) / float(yorig)
		#print "ratio:  " + str(ratio)
		xsize = int(ratio * ysize)
	retDict = {}
	retDict['xsize'] = xsize
	retDict['ysize'] = ysize
	retObj.setResult(retDict)
	retObj.setRetVal(0)
	return retObj
	
def resizeImage (infile, outfile, resize):
	#resize most be in the form of 240x192
	retObj = funcReturn.funcReturn('resizeImage')
	if (os.path.exists ( infile )):
		appleCommand = ["sudo /usr/local/bin/convert -quiet ", infile, "-resize", resize,  outfile]
		retObj = comWrap.comWrapRetObj(appleCommand)
		retVal=retObj.getRetVal()	
		retObj.setName('resizeImage')
		retObj.setRetVal(0)
	else:
		retObj.setError(infile   + " does does not exist")
	return retObj
	
	
def uncompressTif (infile, outfile, tempFile):
	retObj = funcReturn.funcReturn('uncompressTif')
	if (os.path.exists ( infile )):
		appleCommand = "/usr/bin/tiffutil -none " + infile + "  -out " + tempFile
		#print appleCommand
		retObj = comWrap.comWrapString(appleCommand)
		retVal=retObj.getRetVal()
		#print "retVal:  " + str(retVal)
		retObj.setName('uncompressTif')
		if (retVal == 0):	
			#print "retVal == 0"
			fileFunctions.fileDelete(infile)
			retDict=fileFunctions.fileMove2 (tempFile, outfile)
			retObj.setResult(appleCommand)
			retObj.setRetVal(0)
		else:
			#print "retVal == 1"
			retObj.setError(retObj.getStderr())
			retObj.setResult(appleCommand)
			retObj.setRetVal(1)
	else:
		retObj.setError(infile   + " does does not exist")
		retObj.setResult(appleCommand)
	return retObj

def getInfo(img):
	retObj = funcReturn.funcReturn('getInfo')
	try:
		img = Image.open(img)
	except:
		retObj.setRetVal(1)
		e = sys.exc_info()[0]
		retObj.setError(e)
		return retObj
	ysize, xsize = img.size
	retDict = img.info
	retDict['xsize'] = xsize
	retDict['ysize'] = ysize
	retObj.setRetVal(0)
	retObj.setResult(retDict)
	return retObj
	
def getMetadataTiff(tifFile):
	#exiftool needs to be installed for this to work
	#http://www.sno.phy.queensu.ca/~phil/exiftool/
	retObj = funcReturn.funcReturn('getMetadataTiff')
	if (os.path.exists ( tifFile )):
		appleCommand = ["/usr/local/bin/exiftool", tifFile]
		retObj = comWrap.comWrapRetObj(appleCommand)
		retVal=retObj.getRetVal()	
		retObj.setName('getMetadataTiff')
		retObj.setRetVal(0)
	else:
		retObj.setError(tifFile   + " does does not exist")
	return retObj
   
def setMetadataTiff( tifFile, key, value, quote=False, super=False):
	#exiftool needs to be installed for this to work
	#http://www.sno.phy.queensu.ca/~phil/exiftool/
	#exiftool -artist="Phil Harvey" -copyright="2011 Phil Harvey"  /Users/jshipman/Desktop/test.tif 
	if quote == True:
		setValue = '-"' + key + '"="' + value + '"'
	else:
		setValue = "-" + key + "=" + value 
	retObj = funcReturn.funcReturn('setMetadataTiff')
	if (os.path.exists ( tifFile )):
		appleCommand = ["/usr/local/bin/exiftool", setValue, tifFile, "-m -overwrite_original"]
		commandStr = ' '.join(appleCommand)
		#print commandStr	
		
		if key == "Keywords":
			retObj = comWrap.comWrapString(commandStr)
		else:	
			retObj = comWrap.comWrapRetObj(appleCommand, super)
			
		command = str(retObj.getCommand())
		retVal=retObj.getRetVal()	
		retObj.setComment(key + ":\t" + commandStr + "\n")
		retObj.setName('setMetadataTiff')
		retObj.setRetVal(retVal)
		overwriteFile = tifFile + "_original"
		if (os.path.exists ( overwriteFile )):
			os.unlink(overwriteFile)
	else:
		retObj.setError(tifFile   + " does does not exist")
	return retObj

#convert tiff resolution
#   interpolate choices
# 	integer:           The color of the top-left pixel (floor function)
# 	nearest-neighbor:  The nearest pixel to the lookup point (rounded function)
# 	average:           The average color of the surrounding four pixels
# 	bilinear           A double linear interpolation of pixels (the default)
# 	mesh               Divide area into two flat triangular interpolations
# 	bicubic            Fitted bicubic-spines of surrounding 16 pixels
# 	spline             Direct spline curves (colors are blurred)
# 	filter             Use resize -filter settings
#    4000 
def convertTiffRes( tiffIn, interpolate, maxSize = 4000, density = 300):
	retObj = funcReturn.funcReturn('convertTiffRes')
	if (os.path.exists ( tiffIn )):
		retObjInfo= getInfo(tiffIn)
		resultDict = retObjInfo.getResult()
		xsize =	resultDict['xsize']
		ysize = resultDict['ysize'] 
		#print "xsize:  " + str(xsize)
	 	#print "ysize:  " + str(ysize)
		retObjAspect = perserverAspectRation (xsize, ysize, maxSize)
		retDictAspect = retObjAspect.getResult()
		#print "retDictAspect['xsize']:  " + str(retDictAspect['xsize'])
	 	#print "retDictAspect['ysize']:  " + str(retDictAspect['ysize'])
		newXsize=retDictAspect['xsize']
		newYsize=retDictAspect['ysize']
		resize = str(newXsize) + "x" + str(newYsize)
			
		appleCommand='/usr/local/bin/convert -quiet ' + tiffIn + ' -interpolate '+ interpolate +  ' -density '  + str(density) + ' -resize ' + resize + ' ' + tiffIn
		retObj = comWrap.comWrapString(appleCommand)
		retObj.setResult(appleCommand)
		retVal=retObj.getRetVal()
		#print "retVal:  " + str(retVal)
		retObj.setName('uncompressTif')
		if (retVal == 0):	
			#print "retVal == 0"
			#fileFunctions.fileDelete(infile)
			#retDict=fileFunctions.fileMove2 (tempFile, outfile)
			retObj.setResult(appleCommand)
			retObj.setRetVal(0)
		else:
			#print "retVal == 1"
			retObj.setError(retObj.getStderr())
			retObj.setResult(appleCommand)
			retObj.setRetVal(1)
	else:
		retObj.setError(tiffIn   + " does does not exist")
		
	return retObj
	
#convert tiff files to jpg
def convertTiff2Jpg( tiffIn, jpgOut):
	dict = {'function' : 'convertTiff2Jpg'}
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize 500x500 -background white -gravity center -extent 500x500 ' + jpgOut
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
def convertTiff2JpgThumb( tiffIn, jpgOut):
	dict = {'function' : 'convertTiff2JpgThumb'}
	if (os.path.exists ( tiffIn )):
		comWrapCommand='sudo /usr/local/bin/convert -quiet ' + tiffIn + ' -resize 72x72 -background white -gravity center -extent 72x72 ' + jpgOut
		dict['command']= commandwrapper.comWrapCommand
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
			

