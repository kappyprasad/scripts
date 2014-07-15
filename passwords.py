#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



import os,sys,re
import argparse

from _tools.passwords import *

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode')
parser.add_argument('-c', '--clear',    action='store_true',  help='clear cache first')
parser.add_argument('-e', '--env',      action='store',       help='environment name', default='Dev1PC')
parser.add_argument('-u', '--user',     action='store',       help='user name', default='%s'%os.environ['USER'])

args = parser.parse_args()

def main():
    passwords = Passwords(args.env,args.user,args.clear)
    print passwords.password
    return

if __name__ == '__main__': main()
