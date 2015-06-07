#!/usr/bin/env python2.7

import os,sys,re,json
import argparse

from xtermcolor import colorize

from jsonschema import validate

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-d','--delve',   action='store_true', help='delve into schema and rename $ref values')
parser.add_argument('-s','--schema',  action='store',      help='schema name', required=True)
parser.add_argument('json',           action='store',      help='json file')

args = parser.parse_args()

if args.verbose:
    json.dump(vars(args),sys.stderr,indent=4)

def delve(node):
    if type(node) == dict:
        for key in node.keys():
            if type(node[key]) == dict:
                delve(node[key])
            if type(node) == list:
                for child in node:
                    delve(node[key])
            if key == '$ref' and type(node[key]) in [unicode, str]:
                node[key] = node[key].replace('#/schemas/','#/')
                if args.verbose:
                    json.dump(node,sys.stderr,indent=4)
    return

def main():
    with open(args.schema) as fp:
        schema=json.load(fp)
        if args.delve:
            delve(schema)
        fp.close()

    with open(args.json) as fp:
        js=json.load(fp)
        fp.close()

    if type(js) == list:
        for i in range(len(js)):
            j = js[i]
            json.dump(j,sys.stderr,indent=4)
            validate(j,schema)
            if i < len(js)-1:
                sys.stderr.write(',\n')
    else:
        json.dump(js,sys.stderr,indent=4)
        validate(js,schema)

    return

if __name__ == '__main__': main()
