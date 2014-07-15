#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.colours import *
from _tools.eddo import *

horizon=buildHorizon()

def setUp(test):
    #return doBlackAndWhiteSetUp(test)
    return doColourSetUp(test)

def doColourSetUp(test):
    sys.stdout.write('\n%s\n%s%s%s.%s%s%s()\n"""%s"""\n\n'%(
        horizon,
        colours['Purple'],
        test.__class__.__name__,
        colours['Off'],
        colours['Orange'],
        test._testMethodName,
        colours['Off'],
        test._testMethodDoc
    ))
    return

def doBlackAndWhiteSetUp(test):
    sys.stdout.write('\n%s\n%s.%s()\n"""%s"""\n\n'%(
        horizon,
        test.__class__.__name__,
        test._testMethodName,
        test._testMethodDoc
    ))
    return
