#!/usr/bin/env python

import os,sys,re,json,argparse

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',action='store_true')
    parser.add_argument('-u','--username',action='store',help='fake user name')
    parser.add_argument('-p','--password',action='store',help='fake pass word')
    parser.add_argument('filename',action='store',help='the file name')

    group1=parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-x', '--ixml',      action='store',    help='xml input file')
    group1.add_argument('-X', '--oxml',      action='store',    help='xml output file')

    args = parser.parse_args()

    if args.verbose:
        sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))

    return args

args = argue()
print 'verbose =',args.verbose
print 'username=',args.username
print 'password=',args.password
print 'filename=',args.filename


