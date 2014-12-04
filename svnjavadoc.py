#!/usr/bin/python






import sys, re, os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--verbose',  action='store_true',  help='verbose mode'        )
parser.add_argument('file',  nargs='+', action='store',       help='the svn file name'   )

args = parser.parse_args()

words = {
    'created' : 'Date',
    'version' : 'Revision',
    'author'  : 'Author',
}

def mkre(name, tag):
    r = re.compile('^\s*\*\s*@%s .*$'%name)
    p = ' * @%s $%s: $\n'%(name,tag)
    return r,p

reps = {}

for word in words.keys():
    reg,rep = mkre(word,words[word])
    reps[reg] = rep

def main():
    if args.file:
        for arg in args.file:
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

            for line in fp.readlines():
                rep = None
                for reg in reps.keys():
                    if reg.match(line):
                        rep = reps[reg]
                        break
                if rep:
                    op.write('%s'%rep)
                else:
                    op.write('%s'%line)
        
            cmd='svn propset svn:keywords "%s" %s'%(
                ' '.join(map(lambda word: words[word], words.keys()))
                ,arg
            )
            os.system(cmd)

            fp.close()
            op.close()
    return

if __name__ == '__main__': main()

