#!/usr/bin/python





import os,re,sys
import StringIO
import argparse

from _tools.pretty import *
from _tools.eddo import *

parser = argparse.ArgumentParser()

parser.add_argument('-?',              action='help',       help='show this help')
parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')

pgroup = parser.add_mutually_exclusive_group()
pgroup.add_argument('-c','--counter',  action='store_true', help='counter  ~ <count>.....|<repeat...')
pgroup.add_argument('-s','--spaced', action='store_true', help='counter  ~ <count>..... <repeat...')
pgroup.add_argument('-n','--numbers',  action='store_true', help='sequence ~ 1234567890<repeat', default=True)

parser.add_argument('width',           action='store',      help='character width to show', type=int)
                    
args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

def countItOut(tensFormat):
    tens=int(args.width/10)
    frac=args.width%10
    fracFormat='1234567890'
    for i in range(1,tens+1):
        sys.stdout.write('%s'%tensFormat.format(i*10))
    sys.stdout.write('%s\n'%fracFormat[:frac])
    return

def main():
    if args.counter:
        countItOut('{0:.>9}|')
    elif args.spaced:
        countItOut('{0:.>9} ')
    elif args.numbers:
        for i in range(args.width):
            sys.stdout.write('%s'%((i+1)%10))
    print
    return

if __name__ == '__main__': main()


