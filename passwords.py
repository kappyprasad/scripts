#!/usr/bin/env python2.7

import os,sys,re,json,argparse

from Tools.Passwords import *

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode')
    parser.add_argument('-c', '--clear',    action='store_true',  help='clear cache first')
    parser.add_argument('-e', '--env',      action='store',       help='environment name', required=True)
    parser.add_argument('-a', '--app',      action='store',       help='application name', required=True)
    parser.add_argument('-u', '--user',     action='store',       help='user name',        required=True)

    return parser.parse_args()

def main():
    args = argue()
    if args.verbose:
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')
        
    passwords = Passwords(args.env, args.app, args.user, clear=args.clear, verbose=args.verbose)
    print passwords.password
    return

if __name__ == '__main__': main()
