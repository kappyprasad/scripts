#!/usr/bin/env python2.7

import os,sys,re
import argparse

from Tools.Secret import Secret

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',  action='store_true')

kgroup = parser.add_mutually_exclusive_group(required=True)
kgroup.add_argument('-k', '--key',      action='store', help='key as value')
kgroup.add_argument('-f', '--file',     action='store', help='key as file')

parser.add_argument('-t', '--target',   action='store', help='target file to send to')
parser.add_argument('-s', '--source',   action='store', help='source file to read from')

agroup = parser.add_mutually_exclusive_group(required=True)
agroup.add_argument('-e', '--encode',    action='store_true')
agroup.add_argument('-d', '--decode',    action='store_true')

args = parser.parse_args()

def main():
    if args.file:
        fp = open(args.file)
        key = ''.join(fp.readlines())
        fp.close()
        key = key.rstrip()
    if args.key:
        key = args.key

    secret = Secret(key)

    if args.target:
        target = open(args.target,'w')
    else:
        target = sys.stdout

    if args.source:
        source = open(args.source)
    else:
        source = sys.stdin

    input = ''.join(source.readlines())

    if args.encode:
        target.write('%s'%secret.encrypt(input))

    if args.decode:
        target.write('%s'%secret.decrypt(input))

    target.close()
    source.close()

    del secret
    return

if __name__ == '__main__': main()
