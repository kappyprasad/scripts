#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$

import sys,os,re
import argparse
import StringIO
import json

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

group = parser.add_mutually_exclusive_group()
group.add_argument('-e','--eval',    action='store',      help='evaluate a JS expression string', metavar='[\'key\']...')
group.add_argument('-d','--dict',    action='store',      help='evaluate a JS object dict string', metavar='key.key...')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def query(text):
    object = json.loads(text)
    if args.dict:
        expression = dict2eval(args.dict)
        if args.verbose:
            sys.stderr.write('expression=object%s\n'%expression)
        object = eval('object%s'%expression)
    if args.eval:
        object = eval('object%s'%args.eval)
    return object

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
                sys.stderr.write('%s\n'%horizon)
                fp = open(f)
            
            object = query(''.join(fp.readlines()))
            fp.close()

            if inplace:
                fo = open(f,'w')
            else:
                fo = sys.stdout
                                
            prettyPrint(object,colour=colour,output=fo,align=args.align)

            if inplace:
                fo.close()
                print f
    else:
        object = query(''.join(sys.stdin.readlines()))
        prettyPrint(object, colour=colour, align=args.align)

    return

if __name__ == '__main__':main()



