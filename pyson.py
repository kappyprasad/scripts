#!/usr/bin/env python


import sys,os,re
import argparse
import StringIO
import json

from Tools.eddo import *
from Tools.pyson import *
from Tools.pretty import *

horizon = buildHorizon()

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-a','--align',   action='store_true', help='align attributes')
parser.add_argument('-b','--bar',     action='store_true', help='bar between files')
parser.add_argument('-i','--inplace', action='store_true', help='format xml inplace')
parser.add_argument('-c','--colour',  action='store_true', help='show colour output')
parser.add_argument('-t','--text',    action='store_true', help='eval result as text')
parser.add_argument('-n','--name',    action='store_true', help='show file title')
parser.add_argument('-f','--flat',    action='store_true', help='output flat with no indent')
parser.add_argument('-o','--output',  action='store',      help='output file')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

group1 = parser.add_mutually_exclusive_group()
group1.add_argument('-e','--eval',    action='store',      help='evaluate a JS eval',  metavar='\\[key\\[...')
group1.add_argument('-d','--dots',    action='store',      help='evaluate a JS dots',  metavar='key.key...')
group1.add_argument('-x','--xpath',   action='store',      help='evaluate a JS xpath', metavar='/key/key...')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def dump(object,output,colour):
    if args.text:
        output.write('%s'%object)
    elif args.flat:
        json.dump(object,output)
    else:                    
        prettyPrint(object,colour=colour,output=output,align=args.align)
    return

def main():
    global colour, inplace, jpath

    if args.output:
        output = open(args.output,'a')
    else:
        output = sys.stdout

    if args.file and len(args.file) > 0:
        for f in args.file:
            b='%s.bak'%f

            if inplace:
                sys.stderr.write('%s\n'%f)
                try:
                    os.remove(b)
                except:
                    None
                os.rename(f,b)
                fp = open(b)
            else:
                if args.bar:  sys.stderr.write('%s\n'%horizon)
                if args.name: sys.stderr.write('%s\n'%f)
                fp = open(f)
            
            object = query(fp,verbose=args.verbose,xpath=args.xpath,dots=args.dots,brackets=args.eval)
            fp.close()

            if inplace:
                fo = open(f,'w')
            elif args.output:
                fo = output
            else:
                fo = sys.stdout
            
            dump(object,fo,colour)

            if inplace:
                fo.close()
    else:
        object = query(sys.stdin,verbose=args.verbose,xpath=args.xpath,dots=args.dots,brackets=args.eval)
        dump(object,output,colour)

    if args.output:
        output.close()
        
    return

if __name__ == '__main__':main()



