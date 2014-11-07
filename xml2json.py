#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$

import sys,os,argparse,StringIO

import xmltodict,json

parser = argparse.ArgumentParser()

parser.add_argument('-?',              action='help',       help='show this help')
parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
parser.add_argument('-o','--output',   action='store',      help='output to xml file')
parser.add_argument('file',            action='store',      help='files to format', nargs='*')

args = parser.parse_args()

def main():

    if args.output:
        output=open(args.output,'w')
    else:
        output = sys.stdout

    if args.file:
        for file in args.file:
            fp = open(file)
            object = xmltodict.parse('\n'.join(fp.readlines()))
            fp.close()
            json.dump(object,output)
    else:
        fp = StringIO.StringIO('\n'.join(sys.stdin.readlines()))
        json.dump(object.output)
        fp.close()
        
    output.close()
    
    return
    
if __name__ == '__main__': main()

