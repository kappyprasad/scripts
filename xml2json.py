#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




# http://mikekneller.com/kb/python/libxml2python/part1

import sys,os
import argparse
import StringIO

from _tools.xml2json import *

horizon = ''
if 'COLUMNS' in os.environ:
    horizon = '-' * int(os.environ['COLUMNS'])
else:
    horizon = '-' * 80

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-?',              action='help',       help='show this help')
    parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
    parser.add_argument('-c','--colour',   action='store_true', help='show output in colour')
    parser.add_argument('-b','--bar',      action='store_true', help='put horizontal bar inbetween')
    parser.add_argument('-t','--title',    action='store_true', help='display file name as title')
    parser.add_argument('-o','--output',   action='store',      help='output to xml file')
    parser.add_argument('-H','--html',     action='store',      help='output in HTML file')
    parser.add_argument('file',            action='store',      help='files to format', nargs='*')

    args = parser.parse_args()

    colour = args.colour

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
    
    title = args.title

    if args.file:
        for arg in args.file:
            f = arg

            if args.bar:
                print horizon
            if title:
                print f

            fp = open(arg)

            doParse(colour,fp,html,output)

            fp.close()
    else:
        fp = StringIO.StringIO('\n'.join(sys.stdin.readlines()))
        doParse(colour,fp,html,output)
        fp.close()
        
    if foutput:
        output.close()

    return
    
if __name__ == '__main__': main()

