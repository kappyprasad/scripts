#!/usr/bin/env python2.7





import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from Tools.eddo import *
from Tools.colours import *
from Tools.cdata import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-H','--html',     action='store',      help='output colour tags in HTML')
parser.add_argument('lhs',             action='store',      help='left hand side file')
parser.add_argument('rhs',             action='store',      help='right hand side file')

args = parser.parse_args()

def htmlize(part):
    result = part
    if args.html:
        result=convert(part)
        result=result.replace(' ','&nbsp;')
    return result

def main():
    mycolours = getColours(args.html)

    if args.html:
        output=open(args.html,'w')
        output.write('<html><body>\n')
        cr='<br/>\n'
    else:
        output=sys.stdout
        cr='\n'

    lhs = re.compile('^<.*')
    rhs = re.compile('^>.*')

    cmd='/usr/bin/diff %s %s'%(args.lhs,args.rhs)
    output.write('(%s%s%s) -> (%s%s%s) %s'%(
        mycolours['Purple'],args.lhs,mycolours['Off'],
        mycolours['Green'],args.rhs,mycolours['Off'],
        cr
    ))
    process = Popen(cmd,shell=True,stdout=PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.rstrip('\n').rstrip('\r')

        if lhs.match(line):
            output.write(mycolours['Purple'])
        if rhs.match(line):
            output.write(mycolours['Green'])
        output.write('%s%s%s'%(htmlize(line),mycolours['Off'],cr))

    if args.html:
        output.write('</body></html>\n')
        output.close()
        sys.stdout.write('%s\n'%args.html)
   
    return

if __name__ == '__main__': main()
