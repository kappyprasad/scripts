#!/usr/bin/python

import os,sys,re,json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('-u','--username',action='store',help='fake user name')
parser.add_argument('-p','--password',action='store',help='fake pass word')
parser.add_argument('filename',action='store',help='the file name')

args = parser.parse_args()

json.dump(vars(args),sys.stderr,indent=4)
sys.stderr.write('\n')

print 'verbose =',args.verbose
print 'username=',args.username
print 'password=',args.password
print 'filename=',args.filename


