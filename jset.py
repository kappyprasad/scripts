#!/usr/bin/env python


import sys,os,re
import argparse
import StringIO
import json

from Tools.colours import *
from Tools.eddo import *
from Tools.pyson import *
from Tools.pretty import *

horizon = buildHorizon()

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-s', '--show',   action='store_true', help='show changes')
parser.add_argument('-t','--text',    action='store',      help='the text to insert', required=True)
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-e','--eval',    action='store',      help='evaluate a JS expression string', metavar='[\'key\']...')
group.add_argument('-d','--dict',    action='store',      help='evaluate a JS object dict string', metavar='key.key...')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args), colour=True, output=sys.stderr)

def jset(fp):
    object = json.load(fp)
    expression=''
    if args.dict:
        expression = dict2eval(args.dict)
        if args.verbose:
            sys.stderr.write('expression=%s\n'%expression)
    if args.eval:
        expression = args.eval
    old = eval('object%s'%expression)
    keys = expression.split('\[([^\]*)\]')
    child = eval('object%s'%(''.join(keys[:-1])))
    p = re.compile('^\[\"(.*)\"\]$')
    last = keys[-1]
    child[p.match(last).group(1)]=args.text
    new = eval('object%s'%expression)
    if args.show:
        sys.stderr.write('%s-%s=%s%s\n'%(colours['Red'],expression,old,colours['Off']))
        sys.stderr.write('%s+%s=%s%s\n'%(colours['Green'],expression,new,colours['Off']))
    return object

def main():
    if args.file and len(args.file) > 0:
        for f in args.file:
            sys.stdout.write('%s\n'%f)
            b='%s.bak'%f

            try:
                os.remove(b)
            except:
                None
                
            os.rename(f,b)

            fp = open(b)
            object = jset(fp)
            fp.close()

            fo = open(f,'w')
            json.dump(object,fo)
            fo.close()
    else:
        object = jset(sys.stdin)
        json.dump(object,sys.stdout)

    return

if __name__ == '__main__':main()



