#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




import sys, os

from _tools.colours import *

for path in os.environ['PATH'].split(':'):
    if os.path.isdir(path):
        print '+ %s%s%s'%(colours['Green'],path,colours['Off'])
    else:
        print '- %s%s%s'%(colours['Red'],path,colours['Off'])
        
    

