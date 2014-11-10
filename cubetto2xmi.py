#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$

import sys,os,argparse,StringIO

import xmltodict,json

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
        output = open(args.output,'w')
    else:
        output = open(outputEXT,'w')

    fp = open(args.cubetto or args.xmi)
    object = xmltodict.parse('\n'.join(fp.readlines()))
    fp.close()
    json.dump(object,output)
        
    output.close()
    
    return
    
if __name__ == '__main__': main()

