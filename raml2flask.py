#!/usr/bin/env python

import os,sys,re,json
import argparse

import pyraml.parser

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-t','--type',    action='store_true')
parser.add_argument('-o','--output',  action='store', help='save to file output')
parser.add_argument('-k','--key',     action='store', help='specific section key')
parser.add_argument('raml',           action='store', help='raml file')

args = parser.parse_args()

if args.verbose:
        prettyPrint(vars(args),colour=True)

def main():
    raml = pyraml.parser.load(args.raml)
    print type(raml)

    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout

    for key in dir(raml):
        if not key.startswith('_'):
            sys.stdout.write('%s : '%key)
            if args.key and key == args.key:
                json.dump(getattr(raml,key),output,indent=4)
            elif args.type:
                sys.stdout.write('%s'%type(getattr(raml,key)))
            sys.stdout.write('\n')

    if args.output:
        output.close()

    return

if __name__ == '__main__': main()


