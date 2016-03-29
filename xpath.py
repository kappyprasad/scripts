#!/usr/bin/env python

# http://mikekneller.com/kb/python/libxml2python/part1

import sys, re, os, argparse, json

from lxml import etree as ET
#import xml.etree.ElementTree as ET

from Tools.parser import *
from Tools.pretty import *
from Tools.eddo import *

parser = argparse.ArgumentParser()

parser.add_argument('-?',             action='help',       help='show this help')
parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-c','--colour',  action='store_true', help='show colour output')
parser.add_argument('-t','--text',    action='store_true', help='print result as text')
parser.add_argument('-s','--single',  action='store_true', help='display result as a single value')
parser.add_argument('-b','--horizon', action='store_true', help='display horizontal bar between files')
parser.add_argument('-f','--fname',   action='store_true', help='show file name')
parser.add_argument('-o','--output',  action='store',      help='output to file')
parser.add_argument('-e','--element', action='store',      help='use this element as the document root', default='results')
parser.add_argument('-n','--ns',      action='store',      help='added to context ', nargs='*', metavar='prefix:url')
parser.add_argument('-a','--attr',    action='store',      help='get the attr by name')
parser.add_argument('-x','--xpath',   action='store',      help='xpath to apply to the file', nargs='*')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    if args.colour:
        prettyPrint(vars(args), colour=True, output=sys.stderr)
    else:
        sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))

def process(xml=None,file=None,output=sys.stdout,nsp=None):
    #try:
    if True:
        if file:
            tree = ET.parse(file)
            root = tree.getroot()
        elif xml:
            root = ET.fromstring(xml)
        else:
            return
        
        if args.verbose:
            sys.stderr.write('nsp : ')
            if args.colour:
                prettyPrint(nsp,colour=True,output=sys.stderr)
            else:
                sys.stderr.write('%s\n'%json.dumps(nsp,indent=4))

        for xpath in args.xpath:
            if args.single:
                res = root.find(xpath,nsp)
                out = ET.ElementTree(res)
                out.write(output)
            else:
                res = root.findall(xpath,nsp)
                if len(res) == 0:
                    None
                    #output.write('\n')
                else:
                    for r in res:
                        if args.text:
                            output.write('%s\n'%r.text)
                        else:
                            out = ET.ElementTree(r)
                            out.write(output)

    #except:
    #    sys.stderr.write('<!-- exception when parsing -->\n')
    #    if args.verbose:
    #        sys.stderr.write('exc_info : ')
    #        prettyPrint(sys.exc_info(), output=sys.stderr)

    return

def main():

    if args.horizon:
        horizon = buildHorizon()
    else:
        horizon = None

    if args.output:
        output = open(args.output,'w')
        sys.stderr.write('%s\n'%args.output)
    else:
        output=sys.stdout

    nsp = {}
    if args.ns:
        for ns in args.ns:
            p = ns[:ns.index(':')]
            u = ns[ns.index(':')+1:]
            nsp[p] = u

    if args.file:
        for file in args.file:
            if horizon:
                sys.stderr.write('%s\n'%horizon)
            if args.fname:
                if args.text or args.single:
                    sys.stderr.write('%s: '%file)
                else:
                    sys.stderr.write('%s\n'%file)

            process(file=file,output=output,nsp=nsp)
    else:
        xml = sys.stdin.read()
        process(xml=xml,output=output,nsp=nsp)
        
    if args.output:
        output.close()

    return

if __name__ == '__main__' : main()
