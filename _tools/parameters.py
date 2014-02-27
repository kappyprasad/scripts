#!/usr/bin/python

import os,sys,re
import getpass
import getopt

from _tools.eddo import *
from pyson import *

shortargs=[
    'h',
    'u:',
    'p:',
    'v'
]

longargs=[
    'help',
    'username=',
    'password=',
    'verbose'
]

def usage():
    print 'Usage:',sys.argv[0],':',''.join(shortargs),longargs
    return

try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        ''.join(shortargs),
        longargs
    )
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

def getArg(index):
    result = None
    sn = shortargs[index]
    sa = '-%s'%sn.replace(':','')
    la = '--%s'%longargs[index].replace('=','')
    for o,a in opts:
        if o in (sa,la):
            if ':' in sn:
                result = a
            else:
                result = True
            break
    return result

if getArg(0):
    usage()
    sys.exit()

username=getArg(1)
password=getArg(2)
verbose=getArg(3)

if not username:
    username='david.edson'
if not password:
    password=getpass.getpass('Username=%s\nPassword>'%username)

if verbose:
    nestPrint({
        'opts':opts,
        'args':args,
        'user':username,
        'pass':password,
    },colour=True)


