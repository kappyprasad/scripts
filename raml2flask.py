#!/usr/bin/env python2.7

import os,sys,re,json,argparse
import pyraml.parser

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-o','--output',  action='store',      help='save to file output')
parser.add_argument('-d','--dir',     action='store_true', help='directory of keys')
parser.add_argument('-k','--key',     action='store',      help='specific section key')
parser.add_argument('raml',           action='store',      help='raml file')

args = parser.parse_args()

if args.verbose:
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

def main():
    raml = pyraml.parser.load(args.raml)
    sys.stderr.write('%s\n'%type(raml))

    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout

    if args.dir:
        for key in dir(raml):
            if not key.startswith('_'):
                sys.stdout.write('%s\n'%key)

    if args.key:
        for value in getattr(raml,args.key):
            output.write('%s\n'%value)

    if args.output:
        output.close()

    return

if __name__ == '__main__': main()


