#!/usr/bin/env python

import sys,os,re,json,argparse
import getpass, poplib

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
parser.add_argument('-e','--encrypt',  action='store_true', help='use ssl')
parser.add_argument('-S','--server',   action='store',      help='server name', default='mail.tpg.com.au')
parser.add_argument('-P','--port',     action='store',      help='port number', default=110, type=int)
parser.add_argument('-u','--username', action='store',      help='username',    required=False)
parser.add_argument('-p','--password', action='store',      help='password',    required=False)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r', '--read',     action='store',      help='read email to directory')
group.add_argument('-s', '--send',     action='store',      help='write email from directory')

args = parser.parse_args()

if args.verbose:
    sys.stderr.write('args:')
    json.dump(vars(args),sys.stderr,indent=4)

def main():
    if args.encrypt:
        poppy = poplib.POP3_SSL(args.server,args.port)
    else:
        poppy = poplib.POP3(args.server,args.port)

    poppy.user(args.username)
    poppy.pass_(args.password)
    numMessages = len(poppy.list()[1])
    print 'Number of messages = %d'%numMessages

    for message in range(numMessages):
        for stanza in poppy.retr(message+1)[1]:
            if stanza.startswith('Subject:'):
                print stanza
    return

if __name__ == '__main__': main()
