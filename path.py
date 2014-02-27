#!/usr/bin/python

# $Date: 2013-12-13 01:22:40 +1100 (Fri, 13 Dec 2013) $
# $Revision: 7279 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/path.py $
# $Id: path.py 7279 2013-12-12 14:22:40Z david.edson $

import sys, os

from _tools.colours import *

for path in os.environ['PATH'].split(':'):
    if os.path.isdir(path):
        print '+ %s%s%s'%(colours['Green'],path,colours['Off'])
    else:
        print '- %s%s%s'%(colours['Red'],path,colours['Off'])
        
    

