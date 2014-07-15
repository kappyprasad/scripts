#!/usr/bin/python

# $Date: 2014-06-24 19:12:15 +1000 (Tue, 24 Jun 2014) $
# $Revision: 11883 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/BPM/TWBPD.py $
# $Id: TWBPD.py 11883 2014-06-24 09:12:15Z david.edson $


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
class TWBPD(TWProcess):

    def __init__(self,xmi,doc,ctx,sid,package,interfaces):
        TWProcess.__init__(self,xmi,doc,ctx,sid,package,interfaces)

        self.types = {
            # ? : ?
        }

        self.xpathProcess  = '/teamworks/bpd'
        self.xpathStereo   = '/teamworks/bpd/type'
        self.xpathParams   = '/teamworks/bpd/bpdParameter'

        self.xpathStart    = '/teamworks/bpd/BusinessProcessDiagram/pool/lane/flowObject[name="Start"]/position/location'
        self.xpathStartID  = '/teamworks/bpd/BusinessProcessDiagram/pool/lane/flowObject[name="Start"]/outputPort/flow/@ref'

        self.xpathLane     = '/teamworks/bpd/BusinessProcessDiagram/pool/lane'

        self.xpathItem     = 'flowObject'
        self.xpathItemID   = '@id'
        self.xpathItemType = 'component/eventType'
        self.xpathImplType = 'component/implementationType'
        self.xpathLayout   = 'position/location'

        self.xpathLink     = '/teamworks/bpd/BusinessProcessDiagram/flow'
        self.xpathFrom     = '@id'
        self.xpathTo       = 'connection/condition/@id'

        return

