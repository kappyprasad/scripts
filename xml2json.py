#!/usr/bin/python


# https://pypi.python.org/pypi/xmltodict

import sys,os,argparse,StringIO

import xmltodict,json

parser = argparse.ArgumentParser()

parser.add_argument('-?',              action='help',       help='show this help')
parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
parser.add_argument('-r','--reverse',  action='store_true', help='reverse json->xml')
parser.add_argument('-o','--output',   action='store',      help='output to file')
parser.add_argument('-i','--input',    action='store',      help='input from file')

args = parser.parse_args()

def main():

    if args.output:
        output=open(args.output,'w')
    else:
        output = sys.stdout

    if args.input:
        input=open(args.input)
    else:
        input=sys.stdin
        
    if args.reverse:
        object = json.load(input)
        xmltodict.unparse(object,output=output,indent='    ',pretty=True)
    else:
        object = xmltodict.parse(input)
        json.dump(object,output,indent=4)

    output.close()
    input.close()
    
    return
    
if __name__ == '__main__': main()

