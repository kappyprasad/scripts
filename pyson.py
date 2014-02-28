#!/usr/bin/python


import sys,os,re
import argparse
import StringIO

from _tools.eddo import *

horizon = ''
if 'COLUMNS' in os.environ:
    horizon = '-' * int(os.environ['COLUMNS'])
else:
    horizon = '-' * 80

replacements = {
    ':false' : ':False',
    ':true'  : ':True',
    ':null'  : ':None',
    '[null'  : '[None',
    ',null'  : ',None',
}

p=re.compile('^([^\[]*)(\[[^\]]*\])$')

parser = argparse.ArgumentParser()

parser.add_argument('-?',             action='help',       help='show this help')
parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-i','--inplace', action='store_true', help='format xml inplace')
parser.add_argument('-c','--colour',  action='store_true', help='show colour output')
parser.add_argument('file',           action='store',      help='file to parse', nargs='*')

args = parser.parse_args()

if args.verbose:
    nestPrint(vars(args), colour=True, output=sys.stderr)

colour = args.colour

inplace = args.inplace
if inplace:
    colour = False
        
def cleanJSON(lines):
    clean = lines
    for replacement in replacements.keys():
        while replacement in clean:
            clean = clean.replace(replacement,replacements[replacement])
    return eval(clean)

def prettyPrint(lines, colour=colour, output=sys.stdout):
    try:
        json = cleanJSON(lines)
        nestPrint(json, colour=colour, output=output)
    except:
        sys.stderr.write('parse failed, rendering as text\n')
        print lines
    return

def main():
    global colour, inplace, jpath

    if args.file and len(args.file) > 0:
        for f in args.file:
            b='%s.bak'%f

            if inplace:
                try:
                    os.remove(b)
                except:
                    None
                os.rename(f,b)
                output = open(f,'w')
                fp = open(b)
            else:
                print horizon
                fp = open(f)

            lines = '\n'.join(fp.readlines())
            fp.close()

            if inplace:
                fo = open(f,'w')
            else:
                fo = sys.stdout

            prettyPrint(lines,output=fo)

            if inplace:
                fo.close()
                print f
    else:
        lines = '\n'.join(sys.stdin.readlines())
        prettyPrint(lines)

    return

if __name__ == '__main__':main()



