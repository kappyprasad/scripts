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

####################################################################################
class TWClass:

    def __init__(self,xmi,doc,ctx,sid,package):
        self.xmi = xmi
        self.doc = doc
        self.ctx = ctx
        self.sid = sid
        self.package = package
        return

    def exportClasz(self,stereotype,clasz):
        # make seperate class
        cid = getElement(self.ctx,'/teamworks/twClass').prop('id')
        uid = fixTwxID(self.sid,cid)
        twClass = self.xmi.makeClass(clasz,self.package,uid=uid)
        #self.xmi.makeContentTag('twx.id',cid,twClass)
        self.xmi.makeStereotype(stereotype,twClass)

        for property in getElements(self.ctx,'/teamworks/twClass/definition/property'):
            self.exportAttribute(twClass,property,uid)
        return twClass

    def exportAttribute(self,twClass,property,uid):
        name = getElementText(self.ctx,'name',property)
        cref = getElementText(self.ctx,'classRef',property)
        cref = fixTwxRef(self.sid,cref)
        array = getElementText(self.ctx,'arrayProperty',property) == 'true'
        self.xmi.makeAttribute(name,None,None,twClass,tid=cref,array=array)
        self.xmi.makeAssociation(name,None,None,self.package,sid=uid,tid=cref,array=array)
        
