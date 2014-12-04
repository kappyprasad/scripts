#!/usr/bin/python




import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from _tools.pretty import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-s','--shell',    action='store_true', help='verbose mode', default=False)
parser.add_argument('command',         action='store',      help='the svn file name', nargs='*', default='.')

args = parser.parse_args()

def main():

    process = Popen(args.command, shell=args.shell, stdout=PIPE)
    
    while True:
        line = process.stdout.readline()
        if not line: break
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        print line

    del process

    return

if __name__ == '__main__': main()
