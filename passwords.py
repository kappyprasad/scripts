#!/usr/bin/python




import os,sys,re
import argparse

from Tools.passwords import *

if 'HOSTNAME' in os.environ.keys():
    ENV=os.environ['HOSTNAME']
else:
    ENV='localhost'

if 'USER' in os.environ.keys():
    USER=os.environ['USER']
else:
    USER='user'

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode')
parser.add_argument('-c', '--clear',    action='store_true',  help='clear cache first')
parser.add_argument('-e', '--env',      action='store',       help='environment name', default=ENV)
parser.add_argument('-u', '--user',     action='store',       help='user name', default=USER)

args = parser.parse_args()

def main():
    passwords = Passwords(args.env,args.user,args.clear)
    print passwords.password
    return

if __name__ == '__main__': main()
