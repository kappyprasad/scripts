#!/usr/bin/env python2.7




import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from Tools.eddo import *
from Tools.colours import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-f','--force',    action='store_true', help='force diff on binary files')
parser.add_argument('-i','--ignore',   action='store_true', help='ignore content of new files')
parser.add_argument('-H','--html',     action='store',      help='output colour tags in HTML')
parser.add_argument('-r','--revision', action='store',      help='the revision to compare to')
parser.add_argument('-c','--change',   action='store',      help='the change to compare')
parser.add_argument('file',            action='store',      help='the svn file name', nargs='*', default='.')

args = parser.parse_args()

def htmlize(part):
    result = part
    if args.html:
        result=convert(part)
        result=result.replace(' ','&nbsp;')
    return result

def main():
    skyline=buildHorizon('=')
    horizon=buildHorizon()

    mycolours = getColours(args.html)

    if args.html:
        output=open(args.html,'w')
        output.write('<html><body>\n')
        cr='<br/>\n'
    else:
        output=sys.stdout
        cr='\n'

    horizontal = re.compile('^============.*$')
    index      = re.compile('^Index: (.*)$')
    lhs        = re.compile('^\-{3}\s[^\(]*\(([^\)]*)\)$')
    rhs        = re.compile('^\+{3}\s[^\(]*\(([^\)]*)\)$')
    plus       = re.compile('^(\+.*)$')
    minus      = re.compile('^(\-.*)$')

    for file in args.file:

        options = ''
        if args.force:
            options += ' --force'
        if args.revision:
            options += ' -r %s'%args.revision
        if args.change:
            options += ' -c %s'%args.change

        cmd='svn diff %s %s'%(options,file)

        process = Popen(cmd,shell=True,stdout=PIPE)

        while process.stdout:
            line = process.stdout.readline()
            if not line:
                break
            line = line.rstrip('\n')
            line = line.rstrip('\r')
            if horizontal.match(line):
                continue
            m = index.match(line)
            if m:
                fname = m.group(1)
                continue
            m = lhs.match(line)
            if m:
                old = m.group(1)
                continue
            m = rhs.match(line)
            if m:
                new = m.group(1)
                if args.html:
                    output.write('<hr style="height: 4px;;color: black;"/>\n')
                else:
                    output.write('\n%s\n'%skyline)
                output.write('%s%s%s : ( %s- %s%s) -> ( %s+ %s%s)%s'%(
                    mycolours['Orange'], fname, mycolours['Off'], 
                    mycolours['Purple'], old, mycolours['Off'], 
                    mycolours['Green'], new, mycolours['Off'], 
                    cr
                ))
                if args.html:
                    output.write('<hr style="height: 1px"/>\n')
                else:
                    output.write('%s\n'%horizon)
                if old == 'revision 0' and args.ignore:
                    break
                continue
            m = plus.match(line)
            if m:
                output.write('%s%s%s%s'%(
                    mycolours['Green'], htmlize(m.group(1)), mycolours['Off'], 
                    cr
                ))
                continue
            m = minus.match(line)
            if m:
                output.write('%s%s%s%s'%(
                    mycolours['Purple'], htmlize(m.group(1)), mycolours['Off'], 
                    cr
                ))
                continue
            output.write('%s%s'%(htmlize(line),cr))

    if args.html:
        output.write('</body></html>\n')
        output.close()
   
    return

if __name__ == '__main__': main()
