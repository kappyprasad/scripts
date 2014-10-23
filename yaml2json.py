#!/usr/bin/python

import os,re,sys,argparse,yaml

from _tools.pretty import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-c','--colour',  action='store_true', help='in colour')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    prettyPrint(vars(args), colour=True, output=sys.stderr)


def main():
    for file in args.file:
        with open(file) as fp:
            prettyPrint(yaml.load(fp),colour=args.colour)

if __name__ == '__main__': main()
