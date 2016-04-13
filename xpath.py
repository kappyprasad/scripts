#!/usr/bin/env python

# http://mikekneller.com/kb/python/libxml2python/part1

import sys, re, os
import argparse

from Tools.xpath import *
from Tools.parser import *
from Tools.pretty import *
from Tools.eddo import *

parser = argparse.ArgumentParser()

parser.add_argument('-?',             action='help',       help='show this help')
parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-c','--clean',   action='store_true', help='show clean output with root element')
parser.add_argument('-t','--text',    action='store_true', help='print result as text')
parser.add_argument('-s','--single',  action='store_true', help='display result as a single value')
parser.add_argument('-b','--horizon', action='store_true', help='display horizontal bar between files')
parser.add_argument('-f','--fname',   action='store_true', help='show file name')
parser.add_argument('-o','--output',  action='store',      help='output to file')
parser.add_argument('-e','--element', action='store',      help='use this element as the document root', default='results')
parser.add_argument('-n','--ns',      action='store',      help='added to context ', nargs='*', metavar='xmlns:prefix=\"url\"')
parser.add_argument('-x','--xpath',   action='store',      help='xpath to apply to the file')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    prettyPrint(vars(args), colour=True, output=sys.stderr)

def element(xml,rdoc,rctx,nsp):
    (doc,ctx) = getContextFromString(xml)
    element = doc.getRootElement().copyNode(True)
    for ns in nsp.keys():
        ctx.xpathRegisterNs(ns,nsp[ns])
        #element.setProp('xmlns:%s'%ns,'%s'%nsp[ns])
        rdoc.getRootElement().setProp('xmlns:%s'%ns,'%s'%nsp[ns])
    rdoc.getRootElement().addChild(element)
    return

def process(xml,output=sys.stdout,rdoc=None,rctx=None):
    if True: #try
        (doc,ctx,nsp)=getContextFromStringWithNS(xml,args.ns)
        
        if args.verbose:
            sys.stderr.write('nsp : ')
            prettyPrint(nsp,colour=True,output=sys.stderr)

        res = ctx.xpathEval(args.xpath)
        if args.single:
            output.write('%s\n'%res)
        else:
            if len(res) == 0:
                None
                #output.write('\n')
            else:
                for r in res:
                    if args.text:
                        output.write('%s\n'%r.content)
                    elif not args.clean and rdoc and rctx:
                        element('%s'%r,rdoc,rctx,nsp)
                    else:
                        output.write('%s\n'%r)

    if False: #except:
        sys.stderr.write('<!-- exception when parsing -->\n')
        if args.verbose:
            sys.stderr.write('exc_info : ')
            prettyPrint(sys.exc_info(), output=sys.stderr)

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

    (rdoc,rctx) = (None,None)
    if not args.clean:
        (rdoc,rctx) = getContextFromString('<%s/>'%args.element)

    if args.file:
        for file in args.file:
            if horizon:
                sys.stderr.write('%s\n'%horizon)
            if args.fname:
                if args.text or args.single:
                    sys.stderr.write('%s: '%file)
                else:
                    sys.stderr.write('%s\n'%file)

            fp = open(file)
            xml=''.join(fp.readlines())
            fp.close()

            process(xml,output,rdoc,rctx)
    else:
        xml = ''.join(sys.stdin.readlines())
        process(xml,output,rdoc,rctx)

    if not args.clean and not args.text and not args.single:
        output.write('%s'%rdoc)
        
    if args.output:
        output.close()

    return

if __name__ == '__main__' : main()
