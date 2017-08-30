#!/usr/bin/python

import signal, sys
sys.path.append('lib')
from fileFunctions import *      
 
#define the handler function
#Note that this is not executed here, but rather
#  when the associated signal is sent
class termHandler:
	def __init__(self, file):
		self.file = file
	def __call__(signum, frame):
		print "TERM signal handler called.  Exiting."
		#do other stuff to cleanup here
		fileFunctions.fileDelete(self.file)
		sys.exit(1)