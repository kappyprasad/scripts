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
from _tools.eddo import *

import BPM

####################################################################################
parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show help')
parser.add_argument('-i','--indent',  action='store_true', help='indent xml output')
parser.add_argument('-c','--colour',  action='store_true', help='show in colour')
parser.add_argument('-o','--output',  action='store',      help='output.xmi file name', default='.xmi')

fgroup = parser.add_mutually_exclusive_group(required=True)
fgroup.add_argument('-f','--folder',  action='store_true', help='look for *.exploded')
fgroup.add_argument('-a','--app',     action='store_true', help='run as in exploded')

parser.add_argument('-d','--dir',     action='store',      help='the start directory', default='.')

args = parser.parse_args()

####################################################################################
if args.verbose:
    prettyPrint(vars(args),colour=args.colour,output=sys.stderr)
    sys.stderr.flush()

####################################################################################
def main():
    horizon = buildHorizon()

    twx = BPM.TWX(verbose=args.verbose,colour=args.colour)

    if args.folder:
        twx.processFolder(args.dir)
    if args.app:
        twx.processApplication(args.dir)

    doc = twx.exportXMI()

    if args.output:
        sys.stderr.write('%s\n> %s\n'%(horizon,args.output))
        output = open(args.output,'w')
    else:
        output= sys.stdout

    if args.indent:
        input = StringIO.StringIO('%s\n'%doc)
        doParse(False,False,True,input,False,output,False,True)
        input.close()
    else:
        output.write('%s\n'%doc)

    output.close()


    return

if __name__ == '__main__': main()
