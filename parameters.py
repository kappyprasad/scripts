#!/usr/bin/env python

import os,sys,re,json,argparse,logging

def argue():
    parser = argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',action='store_true')
    parser.add_argument('-u','--username',action='store',help='fake user name')
    parser.add_argument('-p','--password',action='store',help='fake pass word')
    parser.add_argument('filename',action='store',help='the file name')

    group1=parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-x', '--ixml',      action='store',    help='xml input file')
    group1.add_argument('-X', '--oxml',      action='store',    help='xml output file')

    args = parser.parse_args()

    if args.verbose:
        sys.stderr.write('%s\n'%json.dumps(vars(args),indent=4))

    return args


def main():
    args = argue()

    level=logging.INFO
    if args.verbose:
        level=logging.DEBUG
        
    logging.basicConfig(level=level)
    #logging.getLogger('spyne.protocol.xml').setLevel(level)

    logging.info('verbose=%s'%args.verbose)
    logging.info('username=%s'%args.username)
    logging.info('password=%s'%args.password)
    logging.info('filename=%s'%args.filename)

    return


if __name__ == '__main__': main()


