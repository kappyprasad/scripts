#!/usr/bin/python

# $Date: 2014-06-24 18:04:17 +1000 (Tue, 24 Jun 2014) $
# $Revision: 11881 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/BPM/TWService.py $
# $Id: TWService.py 11881 2014-06-24 08:04:17Z david.edson $


import sys, re, os, urllib, urllib2, StringIO
import argparse

from _tools.xmi import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.finder import *

from utils import *
from TWProcess import TWProcess

####################################################################################
class TWService(TWProcess):

    def __init__(self,xmi,doc,ctx,sid,package,interfaces):
        TWProcess.__init__(self,xmi,doc,ctx,sid,package,interfaces)

        self.types = {
            '1' : 'Decision Service',
            '3' : 'Human Task',
            '4' : 'Integration Service',
            '5' : 'Deployment Service',
            '6' : 'General Service',
            '7' : 'Advanced Integration Service',
        }

        self.xpathProcess  = '/teamworks/process'
        self.xpathStereo   = '/teamworks/process/processType'
        self.xpathParams   = '/teamworks/process/*[local-name()="processParameter" or local-name()="processVariable"]'

        self.xpathStart    = '/teamworks/process/startPoint/layoutData'
        self.xpathStartID  = '/teamworks/process/startingProcessItemId'

        self.xpathLane     = None

        self.xpathItem     = '/teamworks/process/item'
        self.xpathItemID   = 'processItemId'
        self.xpathItemType = 'tWComponentName'
        self.xpathImplType = None
        self.xpathLayout   = 'layoutData'
        
        self.xpathLink     = '/teamworks/process/link'
        self.xpathFrom     = 'fromProcessItemId'
        self.xpathTo       = 'toProcessItemId'

        return

