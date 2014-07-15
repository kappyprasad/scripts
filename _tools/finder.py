#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/finder.py $
# $Id: finder.py 11546 2014-06-04 06:05:55Z david.edson $

import re,os

def findFiles(path='.', fileOrDir=True, pn='^.*$'):
    files = []
    p = re.compile(pn)
    for f in os.listdir('%s'%path):
        fp = '%s/%s'%(path.rstrip('/'),f)
        if os.path.isfile(fp):
            # is a file
            if p.match(f) and fileOrDir:
                # matches and are looking for files
                files.append(fp)
        elif os.path.isdir(fp):
            #is a dir
            if p.match(f) and not fileOrDir:
                files.append(fp)
            files += findFiles(fp, fileOrDir, pn)
    return files
