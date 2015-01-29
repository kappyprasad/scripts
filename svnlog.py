#!/usr/bin/python





import sys,re,os
import argparse

from subprocess import Popen, PIPE

from Tools.eddo import *
from Tools.colours import *


parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='verbose mode')
parser.add_argument('-r','--revision', action='store',      help='revision to log')
parser.add_argument('file',            action='store',      help='the svn file name', nargs='*', default='.')

args = parser.parse_args()

mycolours = getColours()

p=re.compile('(r\d+)\s\|\s([^\|]+)\s\|\s([^\|]+)\s\|\s(.*)')
l=re.compile('-------')

columns=80
if 'COLUMNS' in os.environ:
    columns = int(os.environ['COLUMNS'])

def logFile(file):
    print '-'*columns
    print '%s%s%s'%(mycolours['Orange'],file,mycolours['Off'])
    print

    versions = {}

    options = ''
    if args.revision:
        options += ' -r %s'%args.revision

    cmd = 'svn log %s %s'%(options,file)

    process = Popen(cmd,shell=True,stdout=PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break

        m = p.match(line)
        line = line.rstrip()
        if m:
            (version,user,timestamp,count) = m.groups()
            versions[timestamp] = {
                'version' : version,
                'user'    : user,
                'count'   : count,
                'body'    : ''
            }
        elif not l.match(line):
            versions[timestamp]['body'] ='%s%s'%(versions[timestamp]['body'],line)

    for timestamp in sorted(versions.keys()):
        record = versions[timestamp]
        line = '%-10s %-20s %s     '%(record['version'],record['user'],timestamp[:19])
        print '%s%s'%(line,record['body'][0:(columns-len(line))])

    return

def main():
    if len(args.file) == 0:
        logFile('')
    else:
        for file in args.file:
            logFile('"%s"'%file)
    return

if __name__ == '__main__': main()
