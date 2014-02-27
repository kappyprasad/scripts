#!/usr/bin/python

# $Date: 2013-12-31 15:53:16 +1100 (Tue, 31 Dec 2013) $
# $Revision: 7553 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/parser.py $
# $Id: parser.py 7553 2013-12-31 04:53:16Z david.edson $

import sys,os
import argparse
import StringIO

from _tools.parser import *

horizon = ''
if 'COLUMNS' in os.environ:
    horizon = '-' * int(os.environ['COLUMNS'])
else:
    horizon = '-' * 80

def doit(colour,areturn,rformat,input,html,output,preserve):
    myParser = MyParser(colour=colour, areturn=areturn, rformat=rformat, html=html, output=output, preserve=preserve)
    try:
        myParser.parser.ParseFile(input)
    except:
        sys.stderr.write('parse failed, rendering as text\n')
        input.seek(0)
        print '\n'.join(input.readlines())
    del myParser
    return

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-?',              action='help',       help='show this help')
    parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
    parser.add_argument('-c','--colour',   action='store_true', help='show output in colour')
    parser.add_argument('-b','--bar',      action='store_true', help='put horizontal bar inbetween')
    parser.add_argument('-i','--inplace',  action='store_true', help='format xml inplace')
    parser.add_argument('-r','--root',     action='store_true', help='indent root attributes')
    parser.add_argument('-a','--attr',     action='store_true', help='indent all attributes')
    parser.add_argument('-t','--title',    action='store_true', help='show title of document')
    parser.add_argument('-p','--preserve', action='store_true', help='preserve line spacing')
    parser.add_argument('-o','--output',   action='store',      help='output to xml file')
    parser.add_argument('-H','--html',     action='store',      help='output in HTML file')
    parser.add_argument('file',            action='store',      help='files to format', nargs='*')

    args = parser.parse_args()

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

            doit(colour,areturn,rformat,fp,html,output,preserve)

            fp.close()

            if inplace:
                output.close()

    else:
        fp = StringIO.StringIO('\n'.join(sys.stdin.readlines()))
        doit(colour,areturn,rformat,fp,html,output,preserve)
        fp.close()
        
    if foutput:
        output.close()

    return
    
if __name__ == '__main__': main()

