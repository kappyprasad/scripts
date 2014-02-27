#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/cdata2null.py $
# $Id: cdata2null.py 7279 2013-12-12 14:22:40Z david.edson $

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
    
    

