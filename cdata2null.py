#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import sys

tokens = {
    '<![CDATA[' : '',
    ']]>' : ''
}

for line in sys.stdin.readlines():
    for key in tokens.keys():
        while key in line:
            line = line.replace(key,tokens[key])
    sys.stdout.write(line)
    sys.stdout.flush()
    
    

