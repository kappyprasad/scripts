#!/usr/bin/env python

'''
An XPath for JSON
 
A port of the Perl, and JavaScript versions of JSONPath
see http://goessner.net/articles/JsonPath/
 
Based on on JavaScript version by Stefan Goessner at:
        http://code.google.com/p/jsonpath/
and Perl version by Kate Rhodes at:
        http://github.com/masukomi/jsonpath-perl/tree/master
'''

import sys, os, re, argparse, json, jsonpath

from Tools.eddo import *
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
parser.add_argument('-p','--path',    action='store',      help='evaluate a jsonpath')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def dump(obj,output,colour):
    if args.text:
        for o in obj:
            output.write('%s\n'%o)
    elif args.flat:
        json.dump(obj,output)
    else:                    
        prettyPrint(obj,colour=colour,output=output,align=args.align)
    return

def main():
    global colour, inplace

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

            obj = None
            try:
                obj = json.load(fp)
                if args.path:
                    obj = jsonpath.jsonpath(obj,args.path)
            except: 
                sys.stderr.write('%s\n'%sys.exc_info()[1])
                    
            fp.close()

            if inplace:
                fo = open(f,'w')
            elif args.output:
                fo = output
            else:
                fo = sys.stdout
            
            dump(obj,fo,colour)

            if inplace:
                fo.close()
    else:
        try:
            obj = json.load(sys.stdin)
            if args.path:
                obj = jsonpath.jsonpath(obj,args.path)
            dump(obj,output,colour)
        except:
            sys.stderr.write('%s\n'%sys.exc_info()[1])

    if args.output:
        output.close()
        
    return

if __name__ == '__main__':main()



