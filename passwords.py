#!/usr/bin/env python

import os,sys,re,json,argparse,logging,string

from Tools.Passwords import *

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode')
    parser.add_argument('-g', '--generate', action='store_true',  help='generate a strong password')
    parser.add_argument('-l', '--length',   action='store',       type=int, default=8)
    parser.add_argument('-c', '--clear',    action='store_true',  help='clear cache first')
    parser.add_argument('-e', '--env',      action='store',       help='environment name', required=True)
    parser.add_argument('-a', '--app',      action='store',       help='application name', required=True)
    parser.add_argument('-u', '--user',     action='store',       help='user name', required=True)
    parser.add_argument('-p', '--password', action='store',       help='save this password')

    return parser.parse_args()

def main():
    args = argue()
    level=logging.WARN
    if args.verbose:
        level=logging.DEBUG
        json.dump(vars(args),sys.stderr,indent=4)
        sys.stderr.write('\n')
    logging.basicConfig(level=level)

    password=args.password

    if args.generate:
        funny = '@!"#$%&()`*+,-/:;<=>?_'
        uppers = string.ascii_uppercase
        lowers = string.ascii_lowercase
        digits = string.digits
        chars =  funny+uppers+lowers+digits
        if args.verbose:
            sys.stderr.write('%s\n'%chars)
        counts = {
            funny : 0,
            uppers : 0,
            lowers : 0,
            digits : 0,
        }
        password = ''
        while len(password) < args.length or any(counts[x] == 0 for x in counts.keys()):
            c = chars[ord(os.urandom(1)) % len(chars)]
            for k in counts.keys():
                if c in k:
                    counts[k] += 1
            password += c
        if args.verbose:
            sys.stderr.write('%s\n'%json.dumps(counts, indent=4))
        
    passwords = Passwords(args.env, args.app, args.user, clear=args.clear, password=password)
    print passwords.password
        
    return

if __name__ == '__main__': main()
