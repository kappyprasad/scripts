#!/usr/bin/env python

import sys,os,re,json,argparse,logging

from Tools.cdata import *

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',    action='store_true')
    parser.add_argument('-r','--reverse',    action='store_true')
    parser.add_argument('-i','--input',      action='store')
    parser.add_argument('-o','--output',     action='store')

    args = parser.parse_args()
    if args.verbose:
        sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))
    return args

def main():
    args = argue()

    level=logging.INFO
    if args.verbose:
        level=logging.DEBUG
        
    logging.basicConfig(level=level)

    input = sys.stdin
    if args.input:
        input=open(args.input)

    output= sys.stdout
    if args.output:
        output = open(args.output,'w')

    if args.reverse:
        xml2cdata(input,output)
    else:
        cdata2xml(input,output)

    if args.output:
        output.close()
    if args.input:
        input.close()
        
    return


if __name__ == '__main__': main()


    
    

