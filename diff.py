#!/usr/bin/env python

import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from Tools.eddo import *
from Tools.colours import *
from Tools.cdata import *

def argue():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
    parser.add_argument('-H','--html',     action='store',      help='output colour tags in HTML')
    parser.add_argument('-r','--recurse',  action='store_true', help='recurse directories, expect lhs to be dir')
    parser.add_argument('-q','--quiet',    action='store_true', help='recurse directories only list files')
    parser.add_argument('lhs',             action='store',      help='left hand side file')
    parser.add_argument('rhs',             action='store',      help='right hand side file')
    return parser.parse_args()
    
def htmlize(part):
    result = part
    if args.html:
        result=convert(part)
        result=result.replace(' ','&nbsp;')
    return result

def compare(lhsf,rhsf,output):
    lhs = re.compile('^<.*')
    rhs = re.compile('^>.*')

    cmd='/usr/bin/diff %s %s'%(lhsf,rhsf)
    output.write('(%s%s%s) -> (%s%s%s) %s'%(
        mycolours['Purple'],lhsf,mycolours['Off'],
        mycolours['Green'],rhsf,mycolours['Off'],
        cr
    ))

    if args.quiet:
        return
    
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

    return

def main():
    global args,mycolours,cr
    
    args = argue()
    mycolours = getColours(args.html)

    if args.html:
        output=open(args.html,'w')
        output.write('<html><body>\n')
        cr='<br/>\n'
    else:
        output=sys.stdout
        cr='\n'

    
    if args.recurse:
        if not os.path.isdir(args.lhs):
            sys.stderr.write('lhs is not a directory')
            return
        if not os.path.isdir(args.rhs):
            sys.stderr.write('rhs is not a directory')
            return

        onlyIn = re.compile('^(Only in )(\S[^:]*):\s+(\S.*)$')
        differ = re.compile('^Files (\S.*) and (\S.*) differ$')
        
        cmd='/usr/bin/diff -rq %s %s'%(args.lhs, args.rhs)
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
            
            match = onlyIn.match(line)
            if match:
                if args.lhs == match.group(2):
                    cfrom=mycolours['Purple']
                if args.rhs == match.group(2):
                    cfrom=mycolours['Green']
                output.write('%s%s%s%s %s%s\n'%(
                    match.group(1),
                    cfrom,match.group(2),
                    mycolours['Red'],match.group(3),mycolours['Off']))
                continue

            match = differ.match(line)
            if match:
                compare(match.group(1),match.group(2),output)

    else:
        compare(args.lhs,args.rhs,output)

    if args.html:
        output.write('</body></html>\n')
        output.close()
        sys.stdout.write('%s\n'%args.html)

    return

if __name__ == '__main__': main()
