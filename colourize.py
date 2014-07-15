#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




import os,sys,re, operator
import argparse

from _tools.colours import *
from _tools.eddo import *
from _tools.pretty import *

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose', action='store_true' )
parser.add_argument('-H', '--html',    action='store',            help='output as html to file')
parser.add_argument('-o', '--orange',  action='store', nargs='*', help='pattern')
parser.add_argument('-g', '--green',   action='store', nargs='*', help='pattern')
parser.add_argument('-b', '--blue',    action='store', nargs='*', help='pattern')
parser.add_argument('-t', '--teal',    action='store', nargs='*', help='pattern')
parser.add_argument('-p', '--purple',  action='store', nargs='*', help='pattern')
parser.add_argument('-r', '--red',     action='store', nargs='*', help='pattern')
parser.add_argument('file',            action='store', nargs='*', help='files or stdin')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args),colour=True)

replacements = []
mycolours = getColours(args.html)

def replace(colour,patterns):
    global replacements
    if not patterns:
        return
    for pattern in patterns:
        p = re.compile('(.*)(%s)(.*)'%pattern)
        c = mycolours[colour]
        replacements.append((p,c))
    return

def colourize(input):
    global replacements
    while True:
        line = input.readline()
        if not line:
            break
        for (p,c) in replacements:
            m = p.match(line)
            if m:
                v = m.group(1)
                line = '%s%s%s%s%s\n'%(
                    m.group(1),
                    c,
                    m.group(2),
                    mycolours['Off'],
                    m.group(3)
                )

        if args.html:
            line = '%s<br/>'%line

        output.write(line)
    return

def main():
    global replacements,output
    replace('Orange', args.orange)
    replace('Green', args.green)
    replace('Blue', args.blue)
    replace('Teal', args.teal)
    replace('Purple', args.purple)
    replace('Red', args.red)

    if args.verbose:
        sys.stderr.write('%s\n'%replacements)

    output = sys.stdout
    if args.html:
        output = open(args.html,'w')
        output.write('<html><body>\n')

    if args.file:
        for file in args.file:
            if args.html:
                output.write('<hr/>\n')
                output.write('<h1>%s</h1>\n'%file)
            fp = open(file)
            colourize(fp)
            fp.close()
    else:
        colourize(sys.stdin)

    if args.html:
        output.write('</body></html>\n')
        output.close()

    return

if __name__ == '__main__': main()
