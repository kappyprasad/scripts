#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


# use getWebSphere.sh to obtain the websphere resource files
####################################################################################
import sys,re,os,argparse,StringIO

from _tools.xmi import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.finder import *

import WebSphere

####################################################################################
parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show help')
parser.add_argument('-d','--dir',     action='store',      help='resource directory',   default='c:/cgu')
parser.add_argument('-o','--output',  action='store',      help='output.xmi file name', default='.xmi')

args = parser.parse_args()

####################################################################################
if args.verbose:
    prettyPrint(vars(args),colour=True,output=sys.stderr)
    sys.stderr.flush()

####################################################################################
def main():
    global files
    
    dt = WebSphere.Tree(verbose=args.verbose)
    #dt.processTypes()
    dt.processDirectory(args.dir)

    if args.output:
        sys.stderr.write('> %s\n'%args.output)
        output = open(args.output,'w')
    else:
        output= sys.stdout

    input = StringIO.StringIO('%s\n'%dt.doc)
    doParse(False,False,True,input,False,output,False,True)
    input.close()
    output.close()
    return

if __name__ == '__main__': main()
