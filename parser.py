#!/usr/bin/python

# http://mikekneller.com/kb/python/libxml2python/part1

import sys,os
import argparse
import StringIO

from Tools.eddo import *
from Tools.parser import *
from Tools.pretty import *

horizon = buildHorizon()

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-?',              action='help',       help='show this help')
    parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
    parser.add_argument('-c','--colour',   action='store_true', help='show output in colour')
    parser.add_argument('-b','--bar',      action='store_true', help='put horizontal bar inbetween')
    parser.add_argument('-n','--nobak',    action='store_true', help='when processing inplace, dont backup file')
    parser.add_argument('-i','--inplace',  action='store_true', help='format xml inplace')
    parser.add_argument('-r','--root',     action='store_true', help='indent root attributes')
    parser.add_argument('-a','--attr',     action='store_true', help='indent all attributes')
    parser.add_argument('-t','--title',    action='store_true', help='show title of document')
    parser.add_argument('-p','--preserve', action='store_true', help='preserve line spacing')
    parser.add_argument('-s','--strip',    action='store_true', help='strip comments')
    parser.add_argument('-o','--output',   action='store',      help='output to xml file')
    parser.add_argument('-H','--html',     action='store',      help='output in HTML file')
    parser.add_argument('file',            action='store',      help='files to format', nargs='*')

    return parser.parse_args()

def main():
    args = argue()
    
    colour = args.colour
    areturn = args.attr
    rformat = args.root

    output = sys.stdout

    foutput = args.output
    if foutput:
        colour = False
        print foutput
        output = open(foutput,'w')

    houtput = args.html
    if houtput:
        html = True
        print houtput
        output = open(houtput,'w')
    else:
        html = False
    
    inplace = args.inplace
    if inplace:
        foutput = None
        colour = False

    title = args.title

    preserve = args.preserve

    comments = not args.strip

    if args.file:
        for arg in args.file:
            f = arg
            b='%s.bak'%f

            if inplace:
                try:
                    os.remove(b)
                except:
                    None
                os.rename(f,b)
                output = open(f,'w')
                fp = open(b)
                print f
            else:
                if args.bar:
                    print horizon
                if title:
                    print f

                fp = open(arg)

            doParse(colour,areturn,rformat,fp,html,output,preserve,comments)

            fp.close()

            if inplace:
                output.close()
                if args.nobak:
                    os.unlink(b)

    else:
        fp = StringIO.StringIO('\n'.join(sys.stdin.readlines()))
        doParse(colour,areturn,rformat,fp,html,output,preserve,comments)
        fp.close()
        
    if foutput:
        output.close()

    return
    
if __name__ == '__main__': main()

