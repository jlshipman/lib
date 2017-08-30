#!/usr/bin/python
try:
	import os
	import pwd
except ImportError:
	print "missing modules for userUtil.py"
	sys.exit(1)

def getUsername():
    return pwd.getpwuid( os.getuid() )[ 0 ]