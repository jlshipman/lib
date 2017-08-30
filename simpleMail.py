#!/usr/bin/python

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import funcReturn

def shortMessage (mailList):
	message = mailList['message']
	from_addr = mailList['from_addr']
	to_addr = mailList['to_addr']
	subject = mailList['subject']


	# Prepare actual message
 	header  = 'From: %s\n' % from_addr
 	header += 'Subject: %s\n\n' % subject
 	message = header + message
	# Send the mail

	server = smtplib.SMTP("smtp.larc.nasa.gov")
	server.sendmail(from_addr, to_addr, message)
	server.quit()
	
def shortMessage2 (mailList):
	retObj = funcReturn.funcReturn('shortMessage2')
	body = mailList['message']
	from_addr = mailList['from_addr']
	to_addr = mailList['to_addr']
	subject = mailList['subject']

	# Prepare actual message
 	message  = 'From: %s\n' % from_addr
 	message += 'To: %s\n' % to_addr
 	message += 'Subject: %s\n\n' % subject
 	message += body
 	
 	#print message
	# Send the mail

	try:
		server = smtplib.SMTP("smtp.larc.nasa.gov")
		server.sendmail(from_addr, to_addr, message)
		retObj.setRetVal(0)
	except SMTPException:
		retObj.setError("Error: unable to send email")
		
	return retObj
	