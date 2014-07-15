#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/svn.py $
# $Id: svn.py 11546 2014-06-04 06:05:55Z david.edson $

import sys, re, os

from subprocess import Popen, PIPE

class SVN(object):

    cmd_status = 'svn status %s %' # options, files
    cmd_diff   = 'svn diff %s %s'  # options, files

    def __init__(self):

        tokens = {
            'A'  : 'Green',
            'M'  : 'Orange',
            '\?' : 'Purple',
            'D'  : 'Red',
            'I'  : 'Teal',
            'C'  : 'Blue',
        }
        self.replacements = {} 
        for key in tokens.keys():
            colour = tokens[key]
            p = re.compile('^(%s.*)$'%key)
            #print p.pattern
            self.replacements[p] = colour


    process = Popen(cmd,shell=True,stdout=PIPE)
    #prettyPrint(process)
    
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        skip = False
        for p in replacements.keys():
            m = p.match(line)
            if m:
                if args.ignore and line[0]=='A':
                    skip = True
                    break
                line = '%s%s%s'%(mycolours[replacements[p]],m.group(1),mycolours['Off'])
                break
        if skip:
            continue
        output.write('%s%s'%(line,cr))

    del process

    if args.html:
        output.write('</body></html>\n')
        output.close()
   
    return

if __name__ == '__main__': main()
