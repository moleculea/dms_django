#!/usr/bin/python
# Filename:using_fork.py

import os, sys, time

print "I'm going to fork now"


while True:
    r, w = os.pipe()
    pid = os.fork()
    if pid:
        
        # parent
        print "pid:", pid
        os.close(w)
        r = os.fdopen(r)
    
        print "parent: reading"
        txt = r.read()
        print txt
        os.waitpid(pid, 0)
    
    else:
        # child
        os.close(r)
        w = os.fdopen(w, 'w')
        print "child:writing"
        w.write("here's some text from the child")
        w.close()
        print "child:closing"
        sys.exit(0)
    time.sleep(1)