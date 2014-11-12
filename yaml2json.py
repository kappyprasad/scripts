#!/usr/bin/python

from _tools.pretty import prettyPrint
import os, re, sys, argparse, yaml, json


parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true', help='show detailed output')
parser.add_argument('-r','--reverse', action='store_true', help='reverse json->yaml')
parser.add_argument('-o','--output',  action='store',      help='output file name')
parser.add_argument('-i','--input',    action='store',      help='file to parse')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args : ')
    prettyPrint(vars(args), colour=True, output=sys.stderr)

def unicode_representer(dumper, uni):
    node = yaml.ScalarNode(tag=u'tag:yaml.org,2002:str', value=uni)
    return node

yaml.add_representer(unicode, unicode_representer)

def main():
    if args.output:
        output = open(args.output,'w')
    else:
        output = sys.stdout
        
    if args.input:
        input = open(args.input)
    else:
        input = sys.stdin
        
    if args.reverse:
        object = json.load(input)
        yaml.dump(object, stream=output)
    else:
        object = yaml.load(input)
        json.dump(object, output)

    output.close()
    input.close()
    
    return
if __name__ == '__main__': main()
