#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$

import sys,os,re,argparse,StringIO

import xmltodict,json

from _tools.pyson import *

import Cubetto

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
parser.add_argument('-o','--output',   action='store',      help='output file')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-c', '--cubetto',  action='store', help='input is cubetto')
group.add_argument('-x', '--xmi',      action='store', help='input is xmi')

args = parser.parse_args()

def main():
    if args.cubetto:
        inputEXT = '.CubettoXML'
        outputEXT = '.xmi'
    if args.xmi:
        inputEXT = '.xmi'
        outputEXT = '.CubettoXML'
        
    if args.output:
        sys.stderr.write('%s\n'%args.output)
        output = open(args.output,'w')
    else:
        sys.stderr.write('%s\n'%outputEXT)
        output = open(outputEXT,'w')

    pattern = re.compile('^.*%s$'%inputEXT)
    file = args.cubetto or args.xmi
    if not pattern.match(file):
        sys.stderr.write('input file %s does not have a valid extension %s'%(file,inputEXT))
        return
    
    fp = open(file)
    object = xmltodict.parse('\n'.join(fp.readlines()))
    fp.close()
    
    # construct XMI model here
    project = Cubetto.Project(object['projects']['project'])
    #done
    
    output.write(project.doc)
        
    output.close()
    
    return
    
if __name__ == '__main__': main()

