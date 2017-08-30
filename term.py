#!/usr/bin/python
import signal, sys
 
#define the handler function
#Note that this is not executed here, but rather
#  when the associated signal is sent
def cleanUp(signum, stack):
        print "cleanUp signal handler called.  Exiting."
        #do other stuff to cleanup here
        sys.exit(-1)