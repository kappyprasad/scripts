#!/usr/bin/env python2.7

import os,re,sys,urllib

for arg in sys.argv[1:]:
    print '<a href="%s">%s</a><br/>'%(urllib.quote(arg),arg)
    
