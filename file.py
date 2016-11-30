#!/usr/bin/env python

import os,re,sys,urllib

for arg in sys.argv[1:]:
    path=os.path.abspath(arg)
    print 'file://{path}'.format(path=urllib.quote(path))
