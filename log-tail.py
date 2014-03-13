#!/usr/bin/python


import sys, re, os, operator
from datetime import *
import argparse

from _tools.xpath import *
from _tools.parser import *
from _tools.eddo import *

verbose = False
files = []
elements = {}
patterns = []
pairs = {}
dump = None
usdate = False
leader = ''
horizon = ''

lep = re.compile('^\[(\d+)/(\d+)/(\d+)\s(\d+):(\d+):(\d+):(\d+)\s(\S+)\]\s([0-9a-f]{8})\s(.*)$')
sep = re.compile('^([^<]*)(<.*)$')
cdp = re.compile('^<!\[CDATA\[(.*)\]\]>$')

dsp = '%Y-%m-%d'
tsp = '%H-%M-%S.%f'

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',   action='store_true', help='versbose mode'                   )
parser.add_argument('-b','--horizon',   action='store_true', help='horizontal bar between messages' )
parser.add_argument('-c','--colour',    action='store_true', help='show in colour'                  )
parser.add_argument('-s','--stubb',     action='store_true', help='stub out date time stamp'        )
parser.add_argument('-a','--attribute', action='store_true', help='format xml attributes'           )
parser.add_argument('-u','--usdate',    action='store_true', help='us date format'                  )
parser.add_argument('-t','--text',      action='store_true', help='text xpath output'               )
parser.add_argument('-e','--element',   action='store',      help='xml element match',              nargs='*')
parser.add_argument('-x','--xpath',     action='store',      help='xpath on xml element'            )
parser.add_argument('-d','--dump',      action='store',      help='dump to file suffix'             )
parser.add_argument('-r','--regex',     action='store',      help='regex patter',                   nargs='*')
parser.add_argument('-p','--pair',      action='store',      help='pair of start:end tags',         nargs='*')
parser.add_argument('files',            action='store',      help='the files to log',               nargs='*')

args = parser.parse_args()

def getElements(args):
    global elements
    elements = { 'start' : [] , 'end' : [] }
    if not args:
        return
    for e in args:
        elements['start'].append(re.compile('.*<%s(|\s.*)(|\/)>.*'%(e)))
        elements['end'].append(re.compile('.*<(/%s|%s/)>.*'%(e,e)))
    if verbose:
        print 'elements='
        for key in elements.keys():
            print '\t%s'%key
            for r in elements[key]:
                print '\t\t%s'%r.pattern
    return

def getPatterns(args):
    global patterns
    patterns = []
    if not args:
        return
    for p in args:
        patterns.append(re.compile('.*%s.*'%(p)))
    if verbose:
        print 'patterns='
        for p in patterns:
            print '\t%s'%p.pattern    

    return

def getPairs(args):
    global pairs
    pairs = { 'start' : [] , 'end' : [] }
    if not args:
        return
    for se in args:
        p = se.split(':')
        if len(p) > 1:
            pairs['start'].append(re.compile('.*%s.*'%(p[0])))
            pairs['end'].append(re.compile('.*%s.*'%(p[1])))
    if verbose:
        print 'pairs='
        for key in pairs.keys():
            print '\t%s'%key
            for r in pairs[key]:
                print '\t\t%s'%r.pattern
    return

def processLine(line):
    global prints, xml, leader, dt, thread, lm, usdate
    if verbose:
        print 'line=%s'%(line)
        
    lm = lep.match(line)
    if lm:
        if usdate:
            months = int(lm.group(1))
            days = int(lm.group(2))
        else:
            days = int(lm.group(1))
            months = int(lm.group(2))
        years = int(lm.group(3))
        hours = int(lm.group(4))
        minutes = int(lm.group(5))
        seconds = int(lm.group(6))
        milisecs = int(lm.group(7))
        timezone = lm.group(8)
        dt = datetime(years,months,days,hours,minutes,seconds,milisecs)
        thread = lm.group(9)
        leader = lm.group(10)
        
    for re in patterns:
        m = re.match(line)
        if m:
            if len(m.groups()) > 0:
                if horizon:
                    sys.stdout.write('%s\n'%horizon)

                dumpIfDump(m.group(1))
                sys.stdout.flush()
            else:
                dumpIfDump(line)
                sys.stdout.flush()
    for re in elements['start'] + pairs['start']:
        if re.match(line):
            prints = True
            if re in elements['start']:
                m = sep.match(line)
                if m:
                    xml = ''
                    line = m.group(2)
                    if '/>' in line:
                        if '<' in leader:
                            i = leader.index('<')
                            leader = leader[:i]
                        printXML(line)
    if prints:
        if xml != None:
            xml += line
        else:
            if lm:
                sys.stdout.write('%s %s %s\n'%(dt,thread,leader))
            else:
                sys.stdout.write(line)
            sys.stdout.flush()
    for re in elements['end'] + pairs['end']:
        if re.match(line):
            prints = False
            if re in elements['end']:
                if xml:
                    while xml[len(xml)-1] != '>':
                        xml = xml[0:-1]
                    printXML(xml)
                xml = None
    sys.stdout.flush()
    return

def printXML(xml):
    global xp, leader, horizon
    if xp:
        (doc,ctx) = getContextFromString(xml)
        for r in ctx.xpathEval(xp):
            if text:
                dumpIfDump(r.content)
            else:
                printSnippetXML('%s'%r)
    else:
        printSnippetXML(xml)
    return

def getDumpFP():
    global dump
    fn = '%s.%s'%(datetime.utcnow().strftime('%s.%s'%(dsp,tsp)),dump)
    print '%s'%fn
    fp = open(fn,'w')
    return fp

def dumpIfDump(text):
    global dump
    if dump:
        fp = getDumpFP()
        fp.write(text)
        fp.close()
    else:
        print text
    return

def printSnippetXML(xml):
    global dump
    if horizon:
        sys.stdout.write('%s\n'%horizon)
        sys.stdout.flush()
    if lm and not stubb:
        sys.stdout.write('%s %s %s\n'%(dt,thread,leader))
        sys.stdout.flush()
    if dump:
        fp = getDumpFP()
    else:
        fp = sys.stdout
    myParser = MyParser(colour=colour, rformat=rformat, output=fp)
    if verbose:
        sys.stdout.write('xml=%s'%xml)
    try:
        myParser.parser.Parse(xml)
    except:
        while xml[:len(xml)-1] == '\n':
            xml = xml.rtrim()
        cdm = cdp.match(xml)
        if cdm:
            xml = cdm.group(1)
        sys.stdout.write('%s\n'%xml)
    del myParser
    if dump:
        fp.close()
    return

def main():
    global prints, verbose, files, xml, horizon, colour, text, xp, stubb, rformat, dump, usdate

    prints = False
    xml = None
    
    if args.horizon:
        horizon = buildHorizon()

    xp = args.xpath
    verbose = args.verbose
    colour = args.colour
    stubb = args.stubb
    rformat = args.attribute
    usdate = args.usdate
    text = args.text
    
    dump = args.dump
    if dump:
        colour = False

    files = args.files

    getElements(args.element)
    getPatterns(args.regex)
    getPairs(args.pair)

    if len(files) == 0:
        while sys.stdin:
            line = sys.stdin.readline()
            processLine(line)
            sys.stdout.flush()
    else:
        for f in files:
            if os.path.isfile(f):
                sys.stderr.write('%s\n'%f)
                fp = open(f)
                for line in fp.readlines():
                    processLine(line)
                fp.close()
            else:
                print 'file %s doesn\'t exist'%f
        
    return

if __name__ == '__main__' : main()
