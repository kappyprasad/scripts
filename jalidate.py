#!/usr/bin/env python

import os,sys,re,json
import argparse

from xtermcolor import colorize

from jsonschema import validate

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true')
parser.add_argument('-s','--schema',  action='store', help='schema name', required=True)
parser.add_argument('json',            action='store', help='json file')

args = parser.parse_args()

if args.verbose:
        prettyPrint(vars(args),colour=True)

def main():
    with open(args.schema) as fp:
        schema=json.load(fp)
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
