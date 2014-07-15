#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



import sys, re, os, copy
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true',            help='verbose mode'         )
parser.add_argument('-u','--undo',    action='store_true', help='remove version tags')
parser.add_argument('file',           action='store',      nargs='+', help='the svn file name'    )

args = parser.parse_args()

words = [
    'Date',
    'Revision',
    'Author',
    'HeadURL',
    'Id'
]

exts = re.compile('^.*\.(py|sh)$')

regs = map(lambda x: re.compile('^# \$(%s):*.*\$'%x), words)

def main():
    if args.file:
        for arg in args.file:
            if not exts.match(arg):
                continue
            
            sys.stderr.write('%s: '%arg)
            
            f = arg
            b='%s.bak'%f
            try:
                os.remove(b)
            except:
                None
            
            os.rename(f,b)
            op = open(f,'w')
            fp = open(b)
            
            top = True
            for line in fp.readlines():
                keep = True
                for re in regs:
                    if re.match(line):
                        keep = False
                        break
                if keep:
                    op.write('%s'%line)
                if top and not args.undo:
                    op.write('\n')
                    op.write('\n'.join(map(lambda x: '# $%s$'%x, words)))
                    op.write('\n')
                    top = False 
            
            try:
                if args.undo:
                    cmd='svn propdel svn:keywords "%s" %s'%(' '.join(words),arg)
                else:
                    cmd='svn propset svn:keywords "%s" %s'%(' '.join(words),arg)
            except:
                None
            
            #os.system(cmd)

            fp.close()
            op.close()
    return

if __name__ == '__main__': main()

