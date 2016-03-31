#!/usr/bin/env python

import os,re,sys,xmltodict,json,argparse

from Tools.parser import *
from Tools.pretty import *
from Tools.jpath import *
from Tools.eddo import *

def argue():
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
    return args
    
def test():    
    global args
    args = argue()

    dir = os.path.dirname(sys.argv[0])
    fp=open('%s/_test/sample.xml'%dir)
    xml=fp.read()
    fp.close()
    
    print
    
    printXML(xml,colour=args.colour,areturn=True)
    
    print
              
    js = xmltodict.parse(xml)
    
    paths = [
        'prefix:root',
        'prefix:child',
    ]
    
    xpath = '/'+'/'.join(paths)
    jp = xpath2eval(xpath)
    
    print ("%s = %s"%(xpath,jp))

    print

    jps = jpath(js,xpath)
    print "as js;"
    prettyPrint(jps,colour=args.colour)
    
    print
    
    results = jpath(js,xpath,xml=True)
    print "as jml;"
    prettyPrint(results,colour=args.colour)

    print 
    
    xml = xmltodict.unparse(results)
    print "as xml;"
    printXML(xml,colour=args.colour,areturn=True)
    
    return

def main():
    global args
    args = argue()
    
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

if __name__ == '__main__': test()
