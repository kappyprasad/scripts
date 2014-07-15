#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



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
        self.xpathItemID   = 'inputPort/flow/@ref'
        self.xpathItemType = 'component/eventType'
        self.xpathImplType = 'component/implementationType'
        self.xpathImplID   = 'component/implementation/attachedActivityId'
        self.xpathLayout   = 'position/location'

        self.xpathLink     = '/teamworks/bpd/BusinessProcessDiagram/pool/lane/flowObject'
        self.xpathFrom     = 'inputPort/flow/@ref'
        self.xpathTo       = 'outputPort/flow/@ref'
        self.linkStyle     = 'TREE=H'

        return

