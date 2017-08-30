#!/usr/bin/python
import unittest
import os, sys
import datetime
import time

curDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(curDir)
dirName = os.path.dirname(curDir)
sys.path.append(dirName)
import timeFunc


class timeFuncTestCase(unittest.TestCase):
	print "Tests for `timeFunc.py`."
	
	def setUp(self):
		pass
        
	def testTimeDuration2(self):
		print "  testTimeDuration2"
		
		print "    Test for live run problem seconds had milliseconds"
		s = '2014-07-23 10:07:01.792471'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-07-24 10:34:36.275581'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 88054
		self.assertEqual(sec, testSec)
		
		print "    Test for complicated difference sec = 2179"
		s = '2014-05-21 11:01:59.077918'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-05-21 11:38:19.010734'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 2179
		self.assertEqual(sec, testSec)
		
		print "    Tests for `diff hours (7200 sec = 2 hours)`."
		s = '2014-05-12 09:59:53.513494'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-05-12 11:59:53.513494'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 7200
		self.assertEqual(sec, testSec)
		
		print "    Tests for `diff min (240 sec = 4 min)`."
		s = '2014-05-12 09:55:53.513494'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-05-12 09:59:53.513494'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 240
		self.assertEqual(sec, testSec)
		
		print "    Tests for `diff sec  (13 sec)`."
		s = '2014-05-12 09:55:40.513494'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-05-12 09:55:53.513494'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 13
		self.assertEqual(sec, testSec)
		
		print "    Tests for `diff days`(259200 sec = 3 days)."
		s = '2014-05-09 09:55:40.513494'
		startTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		s = '2014-05-12 09:55:40.513494'
		endTime = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
		returnDict = timeFunc.timeDuration2( endTime, startTime)
		sec = returnDict['seconds']
		testSec = 24 * 60 * 60 * 3
		self.assertEqual(sec, testSec)
		
	def testTimeDuration(self):
		print ""
		print "  testTimeDuration"
		print "    Tests for `diff sec  (10 sec)`."
		print ""
		ts = time.time()
		testSec = 10
		testSec1 = 12
		begints = round(ts)
		endts = begints + testSec
		returnDict = timeFunc.timeDuration (endts, begints)
		sec = returnDict['seconds']
		self.assertEqual(sec, testSec)
		
	def testStringToTime(self):
		print ""
		print "  stringToTime"
		print "    Tests for converstion wtih 201401050020`."
		print "    should return 2014-01-05 00:20`."
		print ""
		test = "2014-01-05 00:20"
		retVal = timeFunc.stringToTime ("201401050020")
		self.assertEqual(test, retVal)

if __name__ == '__main__':
    unittest.main()