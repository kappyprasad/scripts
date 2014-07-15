#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



import sys,os,re
import argparse

from _tools.eddo import *
from _tools.eddoml import *
from _tools.json import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('file',action='store',help='json file',nargs="*")

args = parser.parse_args()

def process(lines):
    try:
        json = parseJSON(lines)
        print '<json>'
        nestPrintXML(json)
        print '</json>'
    except:
        print lines
    return

def main():
    if args.file:
        for file in args.file:
            fp = open(file)
            lines = '\n'.join(fp.readlines())
            fp.close()
            process(lines)
    else:
        lines = '\n'.join(sys.stdin.readlines())
        process(lines)

if __name__ == "__main__": main()




