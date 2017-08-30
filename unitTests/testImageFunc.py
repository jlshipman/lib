#!/usr/bin/python	
import unittest
import os, sys
import subprocess
import re


curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
curDir=os.getcwd()
import imageFunc
import fileFunctions
import comWrap

class imageFuncTestCase(unittest.TestCase):
 	print "Tests for `imageFunc.py`."

	def setUp(self):
		print ""
		print "setUp"
		print ""
		
# 	def testConvertTiffRes(self):
#  		print "testConvertTiffRes"
#  		# 	integer:           The color of the top-left pixel (floor function)
# 		# 	nearest-neighbor:  The nearest pixel to the lookup point (rounded function)
# 		# 	average:           The average color of the surrounding four pixels
# 		# 	bilinear           A double linear interpolation of pixels (the default)
# 		# 	mesh               Divide area into two flat triangular interpolations
# 		# 	bicubic            Fitted bicubic-spines of surrounding 16 pixels
# 		# 	spline             Direct spline curves (colors are blurred)
# 		# 	filter             Use resize -filter settings
#  		#will need to have know output to test this function"
# 		imagesList = ["/scripts/compare/lib/unitTests/images/R-1987-L-10860.tif", "/scripts/compare/lib/unitTests/images/R-1988-L-05213.tif"] 
# 		interpolateList = ['integer', 'nearest-neighbor', 'average', 'bilinear', 'mesh', 'bicubic', 'spline', 'filter'];
# 		
# 		for i in imagesList:
# 			base=os.path.basename(i)
# 			dirName=os.path.dirname(i)
# 			for x in interpolateList:
# 				resultfile = dirName + "/" + x + base
# 				retDict = fileFunctions.copyFile(i, resultfile)
# 				print "\t\tretVal:  _" + str(retDict['retVal'])  + "_" 
# 				interpolate = "integer"
# 				retObj=imageFunc.convertTiffRes( resultfile, x)
# 				result = retObj.getResult()
# 				retVal = retObj.getRetVal()
# 				comment = retObj.getComment()
# 				stdout = retObj.getStdout()
# 				stderr = retObj.getStderr()
# 				error = retObj.getError()
# 				found = retObj.getFound()
# 				remed = retObj.getRemed()
# 				print "\t\tresult:  _" + str(result)  + "_"
# 				print "\t\tretVal:  _" + str(retVal)  + "_"
# 				print "\t\tcomment: _" + comment + "_"
# 				print "\t\terror:   _" + error + "_"
# 				print "\t\tstdout:  _" + stdout + "_"
# 				print "\t\tstderr:  _" + stderr + "_"
# 				print "\t\tremed:   _" + remed + "_"
# 				print "\t\tfound:   _" + str(found) + "_"	
# 		
# 	def testUncompressTif(self):
#  		print "testUncompressTif"
# 		#will need to have know output to test this function"
# 		img="/scripts/compare/lib/unitTests/images/R-1984-L-02516.tif"
# 		imgTest="/scripts/compare/lib/unitTests/images/testImage.tif"
# 		tempfile="/scripts/compare/lib/unitTests/images/temp.tif"
# 		retDict = fileFunctions.copyFile(img, imgTest)
# 		print "\t\tretVal:  _" + str(retDict['retVal'])  + "_" 
# 		retObj=imageFunc.uncompressTif(imgTest,imgTest,tempfile)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
# 				
# 	def testGetInfo(self):
#  		print "testGetInfo"
# 		#will need to have know output to test this function"
# 		img="/scripts/compare/lib/unitTests/images/R-L-91243.tif"
# 		retObj=imageFunc.getInfo(img)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
		
 	def testSetMetadataTiff(self):
 		print "testSetMetadataTiff"
		#will need to have know output to test this function"
		tifFile="/scripts/photoProcess/lib/unitTests/images/LRC-1999-B701_P-00001.tif"
		key="Keywords"
		#value="LRC-1999-B701_P-00001 1999-L-00001 UH-1 HELICOPTERS AIRCRAFT MODELS A NASA Langley LRC LARC"
		value="LRC-1999-B701_P-00001, 1999-L-00001, UH-1, HELICOPTERS, AIRCRAFT MODELS, NASA, Langley, LRC, LARC"
		#value="asdfasdf"
		quote=True
		super=True
		retObj=imageFunc.setMetadataTiff(tifFile, key, value, quote, super)
		result = retObj.getResult()
		retVal = retObj.getRetVal()
		comment = retObj.getComment()
		stdout = retObj.getStdout()
		stderr = retObj.getStderr()
		error = retObj.getError()
		found = retObj.getFound()
		remed = retObj.getRemed()
		print "\t\tresult:  _" + str(result)  + "_"
		print "\t\tretVal:  _" + str(retVal)  + "_"
		print "\t\tcomment: _" + comment + "_"
		print "\t\terror:   _" + error + "_"
		#print "\t\tstdout:  _" + stdout + "_"
		print "\t\tstderr:  _" + stderr + "_"
		print "\t\tremed:   _" + remed + "_"
		print "\t\tfound:   _" + str(found) + "_"	
		print "\t\tvalue:   _" + str(value) + "_"	
		
#  	def testGetMetadataTiff(self):
#  		print "testGetMetadataTiff"
# 		#will need to have know output to test this function"
# 		tifFile="/scripts/compare/lib/unitTests/images/R-1923-L-00427.tif"
# 		retObj=imageFunc.getMetadataTiff(tifFile)
# 		result = retObj.getResult()
# 		retVal = retObj.getRetVal()
# 		comment = retObj.getComment()
# 		stdout = retObj.getStdout()
# 		stderr = retObj.getStderr()
# 		error = retObj.getError()
# 		found = retObj.getFound()
# 		remed = retObj.getRemed()
# 		print "\t\tresult:  _" + str(result)  + "_"
# 		print "\t\tretVal:  _" + str(retVal)  + "_"
# 		print "\t\tcomment: _" + comment + "_"
# 		print "\t\terror:   _" + error + "_"
# 		print "\t\tstdout:  _" + stdout + "_"
# 		print "\t\tstderr:  _" + stderr + "_"
# 		print "\t\tremed:   _" + remed + "_"
# 		print "\t\tfound:   _" + str(found) + "_"	
		
if __name__ == '__main__':
    unittest.main()
 