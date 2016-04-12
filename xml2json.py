#!/usr/bin/env python


# https://pypi.python.org/pypi/xmltodict

import sys,os,argparse,StringIO

import xml,xmltodict,json

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-?',               action='help',       help='show this help')
    parser.add_argument('-v','--verbose',   action='store_true', help='show detailed output')
    parser.add_argument('-n','--namespace', action='store_true', help='process namespaces')
    parser.add_argument('-c','--cdata',     action='store_true', help='force cdata')
    parser.add_argument('-r','--reverse',   action='store_true', help='reverse json->xml')
    parser.add_argument('-o','--output',    action='store',      help='output to file')
    parser.add_argument('file', nargs='*',  action='store',      help='file to input')

    return parser.parse_args()

def escape_hacked(data, entities={}):
    print entities
    if '<' in data or '>' in data or '&' in data:
        return '<![CDATA[%s]]>' % data
    return escape_orig(data, entities)


def main():
    global args,escape_orig
    args = argue()

    if args.cdata:
        escape_orig = xml.sax.saxutils.escape
        xml.sax.saxutils.escape = escape_hacked

    if args.output:
        output=open(args.output,'w')
    else:
        output = sys.stdout

    if len(args.file) > 0:
        input=open(args.file[0])
    else:
        input=sys.stdin
        
    if args.reverse:
        object = json.load(input)
        xmltodict.unparse(object,output=output,indent='    ',pretty=True)
    else:
        object = xmltodict.parse(input,process_namespaces=args.namespace,force_cdata=args.cdata)
        json.dump(object,output,indent=4)

    output.close()
    input.close()
    
    return
    
if __name__ == '__main__': main()

