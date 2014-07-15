#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




import sys, re, os, copy
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='verbose mode')
parser.add_argument('-u','--undo',    action='store_true', help='un set the executable flag')
parser.add_argument('file',           action='store',      help='the svn file name', nargs='+')

args = parser.parse_args()

exts = re.compile('^.*\.(py|sh|pl)$')

def main():
    if args.file:
        for arg in args.file:
            if not exts.match(arg):
                continue
            sys.stderr.write('%s: '%arg)

            if args.undo:
                cmd='svn propdel svn:executable "%s"'%arg
            else:
                cmd='svn propset svn:executable on "%s"'%arg
            os.system(cmd)
    return

if __name__ == '__main__': main()

