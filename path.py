#!/usr/bin/python





import sys, os

from Tools.colours import *

for path in os.environ['PATH'].split(':'):
    if os.path.isdir(path):
        print '+ %s%s%s'%(colours['Green'],path,colours['Off'])
    else:
        print '- %s%s%s'%(colours['Red'],path,colours['Off'])
        
    

