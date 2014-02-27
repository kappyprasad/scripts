#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/xpath.py $
# $Id: xpath.py 7279 2013-12-12 14:22:40Z david.edson $

import sys, re, os, libxml2
import argparse

from _tools.xpath import *
from _tools.eddo import *

def process(doc,ctx,xpath,ns,single,text):
    for p in ns.keys():
        ctx.xpathRegisterNs(p,ns[p])

    res = ctx.xpathEval(xpath)
    if single:
        print res
    else:
        if len(res) == 0:
            print
        else:
            for r in res:
                if text:
                    print r.content
                else:
                    print r
    return

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-?',             action='help',       help='show this help')
    parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
    parser.add_argument('-c','--clean',   action='store_true', help='show clean output with root element')
    parser.add_argument('-t','--text',    action='store_true', help='print result as text')
    parser.add_argument('-s','--single',  action='store_true', help='display result as a single value')
    parser.add_argument('-b','--horizon', action='store_true', help='display horizontal bar between files')
    parser.add_argument('-f','--fname',   action='store_true', help='show file name')
    parser.add_argument('-e','--element', action='store',      help='use this element as the document root')
    parser.add_argument('-n','--ns',      action='store',      help='added to context ', nargs='*', metavar='prefix:namespace')
    parser.add_argument('-x','--xpath',   action='store',      help='xpath to apply to the file')
    parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

    args = parser.parse_args()

    if args.verbose:
        nestPrint(vars(args), colour=True, output=sys.stderr)

    clean  = args.clean

    text   = args.text
    if text:
        clean = True

    single = args.single
    if single:
        clean = True

    element = args.element
    if not element:
        element = 'results'

    ns = {}
    pn = re.compile('^xmlns:([^=]*)=(.*)$');

    if args.horizon:
        horizon = buildHorizon()
    else:
        horizon = None

    if args.ns:
        for nsp in args.ns:
            m = pn.match(nsp)
            if m:
                ns[m.group(1)]=m.group(2)

    if args.verbose:
        sys.stderr.write('nsp=')
        nestPrint(ns, colour=True, output=sys.stderr)

    xpath = args.xpath

    if not clean:
        print '<%s>'%element

    if args.file:
        for file in args.file:
            if horizon:
                print horizon
            if args.fname:
                if text or single:
                    sys.stdout.write('%s: '%file)
                else:
                    sys.stdout.write('%s\n'%file)
            try:
                (doc,ctx)=getContextFromFile(file)
                process(doc,ctx,xpath,ns,single,text)
            except:
                print '<!-- exception when parsing -->'
                if args.verbose:
                    print '%s'%sys.exc_info()[0]
    else:
        xml = ''.join(sys.stdin.readlines())
        try:
            (doc,ctx)=getContextFromString(xml)
            process(doc,ctx,xpath,ns,single,text)
        except:
            print '<!-- exception when parsing -->'
            if args.verbose:
                print '%s'%sys.exc_info()[0]

    if not clean:
        print '</%s>'%element
        
    return

if __name__ == '__main__' : main()
