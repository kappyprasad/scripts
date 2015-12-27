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
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

group = parser.add_mutually_exclusive_group()
group.add_argument('-e','--eval',    action='store',      help='evaluate a JS expression string', metavar='\\[key\\[...')
group.add_argument('-d','--dict',    action='store',      help='evaluate a JS object dict string', metavar='key.key...')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def query(text,expression=None):
    if args.verbose:
        sys.stderr.write('text=%s[%s], expression=%s\n'%(text,type(text), expression))

    if type(text) == str:
        object = json.loads(text)
    elif type(text) == file:
        object = json.load(text)
    else:
        object = text
    multiple='[*]'
    if expression==None:
        if args.dict:
            expression = dict2eval(args.dict)
        elif args.eval:
            expression = args.eval
        else:
            expression = ''
    if multiple in expression:
        results = []
        parts = expression.split(multiple)
        lhs = '%s"]'%parts[0]
        rhs = '["' + multiple.join(parts[1:])
        rhs = '["%s'%rhs.lstrip('[""]')
        try:
            for result in eval('object%s'%lhs):
                if multiple in rhs:
                    results.append(query(result,rhs))
                else:
                    results.append(result)
        except:
            None
        object = results
    else:
        object = eval('object%s'%expression)
    return object

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
            
            object = query(fp)
            fp.close()

            if inplace:
                fo = open(f,'w')
            else:
                fo = sys.stdout
            
            dump(object,fo,colour)

            if inplace:
                fo.close()
    else:
        object = query(sys.stdin)
        dump(object,sys.stdout,colour)

    return

if __name__ == '__main__':main()



