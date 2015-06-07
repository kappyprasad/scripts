#!/usr/bin/env python2.7

import os,sys,re,json,argparse

from Tools.Passwords import *

if 'HOSTNAME' in os.environ.keys():
    ENV=os.environ['HOSTNAME']
else:
    ENV='localhost'

if 'USER' in os.environ.keys():
    USER=os.environ['USER']
else:
    USER='user'

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode')
    parser.add_argument('-c', '--clear',    action='store_true',  help='clear cache first')
    parser.add_argument('-e', '--env',      action='store',       help='environment name', default=ENV)
    parser.add_argument('-u', '--user',     action='store',       help='user name', default=USER)

    return parser.parse_args()

def main():
    args = argue()
    if args.verbose:
        json.dump(vars(args),sys.stderr,indent=4)
    passwords = Passwords(args.env,args.user,args.clear)
    print passwords.password
    return

if __name__ == '__main__': main()
