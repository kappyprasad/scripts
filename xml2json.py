#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$

# https://pypi.python.org/pypi/xmltodict

import sys,os,argparse,StringIO

import xmltodict,json
from dicttoxml import dicttoxml

parser = argparse.ArgumentParser()

parser.add_argument('-?',              action='help',       help='show this help')
parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
parser.add_argument('-r','--reverse',  action='store_true', help='reverse json->xml')
parser.add_argument('-o','--output',   action='store',      help='output to file')
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
            if args.reverse:
                object = json.load(fp)
                xml = xmltodict.unparse(object)
                output.write('%s'%xml)
            else:
                object = xmltodict.parse('\n'.join(fp.readlines()))
                json.dump(object,output)
            fp.close()
    else:
        if args.reverse:
            object = json.loads('\n'.join(sys.stdin.readlines()))
            xml = xmltodict.unparse(object)
            output.write('%s'%xml)
            None
        else:
            object = xmltodict.parse('\n'.join(sys.stdin.readlines()))
            json.dump(object,output)
        
    output.close()
    
    return
    
if __name__ == '__main__': main()

