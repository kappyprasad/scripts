#!/usr/bin/python

# $Date: 2014-02-07 11:09:21 +1100 (Fri, 07 Feb 2014) $
# $Revision: 8257 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/svnversion.py $
# $Id: svnversion.py 8257 2014-02-07 00:09:21Z david.edson $




import sys, re, os, copy
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose', action='store_true',            help='verbose mode'         )
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
                if top:
                    op.write('\n')
                    op.write('\n'.join(map(lambda x: '# $%s$'%x, words)))
                    op.write('\n')
                    top = False 
        
            cmd='svn propset svn:keywords "%s" %s'%(' '.join(words),arg)
            os.system(cmd)


            fp.close()
            op.close()
    return

if __name__ == '__main__': main()

