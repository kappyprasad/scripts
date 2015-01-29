#!/usr/bin/python




import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from Tools.eddo import *
from Tools.colours import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-H','--html',     action='store',      help='output colour tags in HTML')
parser.add_argument('-m','--message',  action='store',      help='commit message', required=True)
parser.add_argument('file',            action='store',      help='the svn file name', nargs='*', default='.')

args = parser.parse_args()

mycolours = getColours(args.html)

tokens = {
    '(Adding\s+\(bin\)\s+)(.*)'    : 'Green',
    '(Adding\s+)(.*)'              : 'Green',
    '(Sending\s+)(\S.*)'           : 'Orange',
    '(Deleting\s+)(\S.*)'          : 'Red',
    '(Committed revision )(\d+).'  : 'Teal',
}

def main():

    if args.html:
        output=open(args.html,'w')
        output.write('<html><body>\n')
        output.write('<h3>%s<h3>'%os.getcwd())
        cr='<br/>\n'
    else:
        output=sys.stdout
        cr='\n'

    replacements = {} 
    for key in tokens.keys():
        colour = tokens[key]
        p = re.compile('^%s$'%key)
        #print p.pattern
        replacements[p] = colour

    cmd='svn commit -m "%s" %s'%(args.message,' '.join(args.file))

    process = Popen(cmd,shell=True,stdout=PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        for p in replacements.keys():
            m = p.match(line)
            if m:
                line = '%s%s%s%s'%(
                    m.group(1),
                    mycolours[replacements[p]],
                    m.group(2),
                    mycolours['Off']
                )
                break
        output.write('%s%s'%(line,cr))
        output.flush()

    del process

    if args.html:
        output.write('</body></html>\n')
        output.close()
   
    return

if __name__ == '__main__': main()
