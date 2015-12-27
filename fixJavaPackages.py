#!/usr/bin/env python

import sys, re, os

from Tools.finder import *

packagePattern  = re.compile('package\s(\S+);.*')
classPattern = None

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

            match = packagePattern.match(line)
            if match:
                classPattern = re.compile('(.*)(%s)\.([^ \.]+)(.*)'%match.group(1))
            
            m = classPattern.match(line)
            if m:
                (lead,dump,keep,tail) = m.groups()
                op.write('%s%s[]%s\n'%(lead,keep,tail))
            else:
                op.write('%s\n'%line)

        op.close()
        ip.close()
    return

if __name__ == '__main__' : main()

