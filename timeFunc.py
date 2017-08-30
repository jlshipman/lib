#!/usr/bin/python
import datetime

def timeDuration2 (end_time, start_time):
	try:
		time_taken = end_time - start_time # time_taken is in seconds
	except:
		time_taken = 0
	timeTakenStr = str(time_taken)
	checkArray = timeTakenStr.split(',') 
	if len(checkArray) == 1:
		timeTakenStr = checkArray
		days = 0
	else:
		daysText = checkArray[0]
		timeTakenStr =checkArray[1]
		days, text = daysText.split(' ')
 	
 	if days == 0: 
		checkArray = str(timeTakenStr).split('.') 

		if len(checkArray) == 1:
			timeNoTicks = timeTakenStr[0]
			ticks = 0
		else:			
			timeNoTicks, ticks = str(timeTakenStr[0]).split('.')  
 	else:
 		checkArray = str(timeTakenStr).split('.') 
		if len(checkArray) == 1:
			timeNoTicks = checkArray[0]
			ticks = 0
		else:
			timeNoTicks = timeTakenStr
			ticks = timeTakenStr.split('.') 
	
	hours, minutes, secMilli = str(timeNoTicks).split(':')
	test = str(secMilli).split('.')
	if len(test) == 2:
		seconds, milli = str(secMilli).split('.')
	else:
		seconds = secMilli
	minSec = int(minutes) * 60
	hourSec = int(hours) * 60 * 60
	seconds = int(seconds)
	daysSec = int(days) * 60 * 60 * 24
	
	totalSec = minSec + hourSec + seconds + daysSec

	printHours = hours
	printMins = minutes
	printSec = seconds
	printDays = days
	
	dict = {'daysSec': daysSec, 'hours': hours, 'minutes': minutes, 'printDays': printDays, 'printHours': printHours, 'printMins': printMins, 'printSec': printSec, 'seconds': totalSec} 
	return dict
	
def timeDuration (end_time, start_time):
	try:
		time_taken = end_time - start_time # time_taken is in seconds
	except:
		time_taken = 0
	hours, rest = divmod(time_taken,3600)
	minutes, seconds = divmod(rest, 60)
	printHours = int (round ( hours, 0 ))
	printMins = int (round ( minutes, 0 ))
	dict = {'hours': hours, 'minutes': minutes, 'printHours': printHours, 'printMins': printMins, 'seconds': time_taken} 
	return dict
	
def stringToTime ( timeStr ):
	#expect string to be YYYYMMDDHHMM
	y = timeStr[0:4]
	m = timeStr[4:6]
	d = timeStr[6:8]
	h = timeStr[8:10]
	min = timeStr[10:12]
	return y + "-" + m + "-" + d + " " + h + ":" + min
	
def time1BiggerThantime2 ( time1, time2 ):
	start = datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M')
	tocompare = datetime.datetime.strptime(time2,'%Y-%m-%d %H:%M')
	return start > tocompare # False

def currentTimeString ():
	now = datetime.datetime.now()
	return(now.strftime("%Y-%m-%d_%H:%M"))