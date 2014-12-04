#!/usr/bin/python





import os,sys,re
import argparse

from _tools.pretty import *
from _tools.eddo import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('-u','--username',action='store',help='fake user name')
parser.add_argument('-p','--password',action='store',help='fake pass word')
parser.add_argument('filename',action='store',help='the file name')

args = parser.parse_args()

prettyPrint(vars(args),colour=True)

print 'verbose =',args.verbose
print 'username=',args.username
print 'password=',args.password
print 'filename=',args.filename


