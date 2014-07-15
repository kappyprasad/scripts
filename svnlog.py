#!/usr/bin/python

import sys,re,os

from _tools.eddo import *

p=re.compile('(r\d+)\s\|\s([^\|]+)\s\|\s([^\|]+)\s\|\s(.*)')
l=re.compile('-------')

columns=80
if 'COLUMNS' in os.environ:
    columns = int(os.environ['COLUMNS'])

def logFile(file):
    print '-'*columns
    print file
    print

    versions = {}

    (fi,fo,fe) = os.popen3('svn log %s'%file)
    fi.close();

    for line in fo.readlines(): 
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

    fo.close()
    fe.close()

    for timestamp in sorted(versions.keys()):
        record = versions[timestamp]
        line = '%-10s %-20s %s     '%(record['version'],record['user'],timestamp[:19])
        print '%s%s'%(line,record['body'][0:(columns-len(line))])

    return

def main():
    if len(sys.argv) == 1:
        logFile('')
    else:
        for file in sys.argv[1:]:
            logFile('"%s"'%file)
    return

if __name__ == '__main__': main()
