#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/parameters.py $
# $Id: parameters.py 7279 2013-12-12 14:22:40Z david.edson $

import os,sys,re
import argparse

from _tools.eddo import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('-u','--username',action='store',help='fake user name')
parser.add_argument('-p','--password',action='store',help='fake pass word')
parser.add_argument('filename',action='store',help='the file name')

args = parser.parse_args()

nestPrint(vars(args),colour=True)

print 'verbose =',args.verbose
print 'username=',args.username
print 'password=',args.password
print 'filename=',args.filename


