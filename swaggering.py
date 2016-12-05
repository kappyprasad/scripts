#!/usr/bin/env python

import os, sys, re, xmltodict, json, yaml, argparse, logging

from swagger_parser import SwaggerParser

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose',   action='store_true')
    parser.add_argument('-u', '--username',  action='store',       help='your user name')
    parser.add_argument('-p', '--password',  action='store',       help='your pass word')

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-x', '--xml',       action='store_true',  help='xml output')
    group1.add_argument('-j', '--json',      action='store_true',  help='json output')
    group1.add_argument('-y', '--yaml',      action='store_true',  help='yaml output')

    subparsers = parser.add_subparsers(       help='commands and arguments')
    
    parserA = subparsers.add_parser('paths')
    parserA.set_defaults(command='paths')
    parserA.add_argument('swagger',          action='store')
    parserA.add_argument('-o', '--output',   action='store', help='save to file')
    
    parserB = subparsers.add_parser('b',     help='help for command b')
    parserB.set_defaults(command='b')
    parserB.add_argument('nameB',            help='name for b')
    parserB.add_argument('-B', '--optB',     help='opt for b')
    
    args = parser.parse_args()
    if args.verbose: json.dump({'args':vars(args)}, sys.stderr,indent=4)
    return args


def main():
    args = argue()

    level = logging.WARN
    if args.verbose:
        level = logging.DEBUG
        
    logging.basicConfig(level=level)
    
    if args.command == 'paths':
        swaggering = SwaggerParser(swagger_path=args.swagger)
        if args.output:
            output = open(args.output,'w')
        else:
            output = sys.stdout
            
        for path in swaggering.paths:
            output.write('%s\n'%path)

        if args.output:
            output.close()
    
    # Get an example of a correct body for a path
    #print(parser.get_send_request_correct_body('/users', 'post'))

    return

if __name__ == '__main__':
    main()
