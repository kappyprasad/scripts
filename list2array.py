#!/usr/bin/env python

import sys, re, os

from Tools.finder import *

uidPattern  = re.compile('.*static final long serialVersionUID = 1L.*') 
listPattern = re.compile('^(.*)(java.util.List)<([^>]+)>(.*)$')

def main():
    for f in findFiles(path='.',fileOrDir=True,pn='^.*\.java$'):

        sys.stderr.write('%s\n'%f)
        b = '%s.bak'%f
        os.rename(f,b)
        ip = open(b)
        op = open(f,'w')

        for line in ip.readlines():
            line = line.rstrip('\r')
            line = line.rstrip('\n')

            if uidPattern.match(line):
                continue
            
            m = listPattern.match(line)
            if m:
                (lead,dump,keep,tail) = m.groups()
                op.write('%s%s[]%s\n'%(lead,keep,tail))
            else:
                op.write('%s\n'%line)

        op.close()
        ip.close()
    return

if __name__ == '__main__' : main()

