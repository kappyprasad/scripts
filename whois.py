#!/usr/bin/python




import sys, re, os, copy
import argparse

from subprocess import Popen, PIPE

from _tools.pretty import *

defaults=[
    'dn',
    'cn',
    'uid',
    'name',
    'displayName',
    'mail'
]

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-a','--all',      action='store_true', help='all fields')
parser.add_argument('-q','--query',    action='store',      help='query string')
parser.add_argument('-o','--output',   action='store',      help='output file')
parser.add_argument('-c','--columns',  action='store',      help='columns arguments', nargs='*', default=defaults)

ogroup = parser.add_mutually_exclusive_group(required=True)
ogroup.add_argument('-x','--xml',      action='store_true', help='text output')
ogroup.add_argument('-t','--text',     action='store_true', help='xml output')

args = parser.parse_args()

if args.verbose:
    prettyPrint(vars(args))

host='dynam150.clarence.sirca.org.au'
port=50389
baseDN='dc=openam,dc=forgerock,dc=org'
username='cn=Directory Manager'
password='password1'

def col(output,name,value):
    if args.xml:
        output.write('<%s><![CDATA[%s]]></%s>\n'%(name,value,name))
    else:
        output.write('%s=%s\n'%(name,value))        
    return

def main():

    if args.output:
        sys.stderr.write('%s\n'%args.output)
        output = open(args.output,'w')
    else:
        output = sys.stdout

    if args.xml:
        output.write('<rows>\n')

    rowStart = re.compile('^dn:.*$')
    allFields = re.compile('^([^: #]*): (.*)$')

    columns = {}

    query=''
    if args.query:
        query = args.query

    for column in args.columns:
        columns[column] = re.compile('^%s: (.*)$'%column)

    cmd = 'ldapsearch -H ldap://%s:%s -b "%s" -D "%s" -w "%s" %s'%(
        host,
        port,
        baseDN,
        username,
        password,
        args.query
    )

    if args.verbose:
        sys.stderr.write('%s\n'%cmd)

    process = Popen(cmd, shell=True, stdout=PIPE)

    waitingStart = True

    while True:
        line = process.stdout.readline()
        if not line: break
        line = line.rstrip('\n')
        line = line.rstrip('\r')

        if args.verbose:
            sys.stderr.write('%s\n'%line)

        if rowStart.match(line) and args.xml:
            if not waitingStart:
                output.write('\t</row>\n')
            output.write('\t<row>\n')
            waitingStart = False

        if args.all:
            m = allFields.match(line)
            if m:
                col(output,m.group(1),m.group(2))
            continue

        for column in columns.keys():
            m = columns[column].match(line)
            if m:
                col(output,column,m.group(1))

    del process

        
    if args.xml:
        if not waitingStart:
            output.write('\t</row>\n')
        output.write('</rows>\n')
    
    if args.output:
        output.close()

    return

if __name__ == '__main__': main()
