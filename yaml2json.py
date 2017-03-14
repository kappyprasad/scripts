#!/usr/bin/env python

import os, re, sys, argparse, yaml, json

from datetime import datetime, timedelta

from Tools.PrettyYAML import *
from Tools.pretty import prettyPrint


#_____________________________________________________
def argue():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
    parser.add_argument('-r','--reverse', action='store_true', help='reverse json->yaml')
    parser.add_argument('-f','--flow',    action='store_true', help='default flow style')
    parser.add_argument('-o','--output',  action='store',      help='output file name')
    parser.add_argument('-i','--input',   action='store',      help='files to parse', nargs='*', default=[])
    parser.add_argument('file',           action='store',      help='files to parse', nargs='*')
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-e','--eval',    action='store',      help='evaluate a JS expression string', metavar='\\[key\\[...')
    group.add_argument('-d','--dict',    action='store',      help='evaluate a JS object dict string', metavar='key.key...')
    
    args = parser.parse_args()
    
    if args.verbose:
        sys.stderr.write('args : ')
        prettyPrint(vars(args), colour=True, output=sys.stderr)
        
    return args
        
loadRepresenters()

#_____________________________________________________
def query(object):
    if args.dict:
        expression = dict2eval(args.dict)
        if args.verbose:
            sys.stderr.write('expression=object%s\n'%expression)
        object = eval('object%s'%expression)
    if args.eval:
        object = eval('object%s'%args.eval)
    return object
    
#_____________________________________________________
def process(input,output):
    if args.reverse:
        object = json.load(input)
        object = query(object)
        yaml.dump(object,stream=output,indent=4,default_flow_style=args.flow)
    else:
        object = yaml.load(input)
        object = query(object)
        json.dump(object, output, indent=4)
    input.close()
    return

#_____________________________________________________
def main():
    global args
    args = argue()
    
    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout

    files = args.input + args.file
    if len(files) == 0:
        process(sys.stdin,output)
    else:
        for file in files:
            process(open(file),output)
        
    if args.output:
        output.close()
    
    return

if __name__ == '__main__': main()




