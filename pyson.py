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
    json = cleanJSON(text)
    if args.dict:
        expression = ''.join(map(lambda x : '["%s"]'%x, args.dict.split('.')))
        if args.verbose:
            sys.stderr.write('expression=json%s\n'%expression)
        json = eval('json%s'%expression)
    if args.eval:
        json = eval('json%s'%args.eval)
    return json

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
            
            json = query(''.join(fp.readlines()))
            fp.close()

            if inplace:
                fo = open(f,'w')
            else:
                fo = sys.stdout
                                
            prettyPrint(json,colour=colour,output=fo,align=args.align)

            if inplace:
                fo.close()
                print f
    else:
        json = query(''.join(sys.stdin.readlines()))
        prettyPrint(json, colour=colour, align=args.align)

    return

if __name__ == '__main__':main()



