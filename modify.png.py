#!/usr/bin/env python2.7

import os,re,sys,argparse
from subprocess import Popen, PIPE, call

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',   action='store_true', help='verbose')
parser.add_argument('-b','--backup',    action='store',      help='backup dir')
parser.add_argument('-W','--wMultiply', action='store', type=float, default=1)
parser.add_argument('-H','--hMultiply', action='store', type=float, default=1)
parser.add_argument('-X','--xOffset',   action='store', type=int,   default=0)
parser.add_argument('-Y','--yOffset',   action='store', type=int,   default=0)
parser.add_argument('file',             action='store',      help='png files', nargs='*')

args = parser.parse_args()

def size(name):
    pattern = re.compile('^%s\sPNG\s(\d+x\d+)\s.*$'%name)
    process = Popen('identify %s'%name ,shell=True,stdout=PIPE)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        match = pattern.match(line)
        if match:
            (width,height) = match.group(1).split('x')
    del process
    del pattern
    return (int(width),int(height))

def crop(name,width,height,x,y):
    if args.verbose:
        sys.stderr.write('%s %dx%d+%d+%d\n'%(name,width,height,x,y))
    if args.backup:
        call(['cp','%s'%name,'%s/%s'%(args.backup,name)])
    geometry='%dx%d+%d+%d'%(
        int(width*args.wMultiply),
        int(height*args.hMultiply),
        int(args.xOffset),
        int(args.yOffset)
    )
    call(['mogrify','-crop', geometry, '+repage', name])
    return

def main():
    if args.backup:
        if not os.path.isdir(args.backup):
            os.makedirs(args.backup)
    for name in args.file:
        name = name.lstrip('./')
        sys.stderr.write('%s\n'%name)
        (width,height) = size(name)
        crop(name,width,height,0,0)
    return

if __name__ == '__main__': main()
