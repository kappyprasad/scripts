#!/usr/bin/env python



# use getWebSphere.sh to obtain the websphere resource files
####################################################################################
import sys,re,os,argparse,StringIO

from Tools.xmi import *
from Tools.xpath import *
from Tools.parser import *
from Tools.pretty import *
from Tools.finder import *

import WebSphere

####################################################################################
parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show help')
parser.add_argument('-i','--indent',  action='store_true', help='indent xml output')
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
    dt.processDirectory(args.dir)
    doc = dt.export()

    if args.output:
        sys.stderr.write('> %s\n'%args.output)
        output = open(args.output,'w')
    else:
        output= sys.stdout

    if args.indent:
        input = StringIO.StringIO('%s\n'%doc)
        doParse(False,False,True,input,False,output,False,True)
        input.close()
    else:
        output.write('%s'%doc)

    output.close()
    return

if __name__ == '__main__': main()
