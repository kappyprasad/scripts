#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




import sys,os,re
import argparse
import StringIO

from _tools.eddo import *
from _tools.pyson import *
from _tools.pretty import *

horizon = buildHorizon()

parser = argparse.ArgumentParser()

parser.add_argument('-?',             action='help',       help='show this help')
parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-a','--align',   action='store_true', help='align attributes')
parser.add_argument('-i','--inplace', action='store_true', help='format xml inplace')
parser.add_argument('-c','--colour',  action='store_true', help='show colour output')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def main():
    global colour, inplace, jpath

    if args.file and len(args.file) > 0:
        for f in args.file:
            b='%s.bak'%f

            if inplace:
                try:
                    os.remove(b)
                except:
                    None
                os.rename(f,b)
                output = open(f,'w')
                fp = open(b)
            else:
                print horizon
                fp = open(f)

            lines = cleanJSON(''.join(fp.readlines()))
            fp.close()

            if inplace:
                fo = open(f,'w')
            else:
                fo = sys.stdout

            prettyPrint(lines,colour=colour,output=fo,align=args.align)

            if inplace:
                fo.close()
                print f
    else:
        json = cleanJSON(''.join(sys.stdin.readlines()))
        prettyPrint(json, colour=colour, align=args.align)

    return

if __name__ == '__main__':main()



