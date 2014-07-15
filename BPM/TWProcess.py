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
class TWProcess(object):

    #override these in subclass

    types = {
        # 'number' : 'Name'
    }

    xpathProcess  = None 
    xpathStereo   = None
    xpathParams   = None

    xpathStart    = None
    xpathStartID  = None

    xpathLane     = None

    xpathItem     = None
    xpathItemID   = None
    xpathItemType = None
    xpathImplType = None
    xpathImplID   = None
    xpathLayout   = None

    xpathLink     = None
    xpathFrom     = None
    xpathTo       = None
    linkStyle     = None

    def __init__(self,xmi,doc,ctx,sid,package,interfaces):
        self.xmi = xmi
        self.doc = doc
        self.ctx = ctx
        self.sid = sid
        self.package = package
        self.interfaces = interfaces
        return

    def exportProcess(self,name):
        # make seperate class
        cid = getElement(self.ctx,self.xpathProcess).prop('id')
        uid = fixTwxID(self.sid,cid)
        stereotype = getElementText(self.ctx,self.xpathStereo)
        if stereotype in self.types.keys():
            stereotype = self.types[stereotype]

        self.diagramPackage = self.xmi.makePackage(name,self.package)

        self.twProcess = self.xmi.makeClass(name,self.diagramPackage,uid=uid)
        self.xmi.makeStereotype(stereotype,self.twProcess)

        self.params = {
            'input'   : self.xmi.makeClass('%s_Input'%name,self.interfaces),
            'output'  : self.xmi.makeClass('%s_Output'%name,self.interfaces),
            'private' : self.xmi.makeClass('%s_Private'%name,self.interfaces),
        }

        for p in self.params.keys():
            self.xmi.makeAttribute(p,None,None,self.twProcess,tid=self.params[p].parent.prop('xmi.id'))
            self.xmi.makeAssociation('interface',self.twProcess,self.params[p],self.package)

        for property in getElements(self.ctx,self.xpathParams):
            self.exportAttribute(property)

        self.activityModel = self.xmi.makeActivityModel(name,self.diagramPackage)
        self.activityDiagram = self.xmi.makeActivityDiagram(name,self.diagramPackage)

        self.pids = {}

        startState = self.xmi.makeActivityStartState('Start',self.activityModel)
        layout = getElement(self.ctx,self.xpathStart)
        if layout != None:
            geometry='Left=%d;Top=%d;Right=%d;Bottom=%d;'%(
                int(layout.prop('x')),
                int(layout.prop('y')),
                int(layout.prop('x'))+10,
                int(layout.prop('y'))+10,
            )
        else:
            geometry=None
        self.xmi.addDiagramState(startState,self.activityDiagram,geometry=geometry)

        if self.xpathLane != None:
            # this is for BPDs
            offset = 0
            for lane in getElements(self.ctx,self.xpathLane):
                name = getElementText(self.ctx,'name',lane)
                height = int(getElementText(self.ctx,'height',lane))
                swimLane = self.xmi.makeActivitySwimLane(name,self.activityModel)
                geometry='Left=0;Top=%d;Right=3000;Bottom=%d;'%(
                    offset,
                    offset+height,
                )
                self.xmi.addDiagramState(swimLane,self.activityDiagram,geometry=geometry,style='Dockable=on;')
                pgr = getElementText(self.ctx,'attachedParticipant',lane)
                pgr = fixTwxRef(self.sid,pgr)
                self.xmi.makeAssociation('participant',None,None,self.diagramPackage,sid=swimLane.prop('xmi.id'),tid=pgr)

                for item in getElements(self.ctx,self.xpathItem,lane):
                    state = self.processItem(item,offset=offset)
                    self.xmi.addActivityToLane(item,lane)

                offset += height

        else:
            #this is for regular processes
            for item in getElements(self.ctx,self.xpathItem):
                self.processItem(item)

        sid = getElementText(self.ctx,self.xpathStartID)
        if sid in self.pids.keys():
            transition = self.xmi.makeTransition(startState,self.pids[sid],self.activityModel)
            self.xmi.addDiagramElement(transition,self.activityDiagram,style=self.linkStyle)

        for link in getElements(self.ctx,self.xpathLink):
            name = link.prop('name')

            if self.xpathFrom[0] == '@':
                fid = link.prop(self.xpathFrom[1:])
            else:
                fid = getElementText(self.ctx,self.xpathFrom,link)

            if self.xpathTo[0] == '@':
                tid = link.prop(self.xpathTo[1:])
            else:
                tid = getElementText(self.ctx,self.xpathTo,link)

            if fid in self.pids.keys() and tid in self.pids.keys():
                transition = self.xmi.makeTransition(self.pids[fid],self.pids[tid],self.activityModel,name=name)
                self.xmi.addDiagramElement(transition,self.activityDiagram,style=self.linkStyle)

        return self.twProcess

    def processItem(self,item,offset=0):
        name = getElementText(self.ctx,'name',item)
        if self.xpathItemID[0] == '@':
            pid = item.prop(self.xpathItemID[1:])
        else:
            pid = getElementText(self.ctx,self.xpathItemID,item)
        if pid != None and not 'bpdid:' in pid:
            pid = fixTwxRef(self.sid,pid)

        type = getElementText(self.ctx,self.xpathItemType,item)
        if self.xpathImplType != None:
            impl = getElementText(self.ctx,self.xpathImplType,item)
        else:
            impl = None
        if type == '1':
            state = None #ignore extra start message
        elif type == 'ExitPoint' or type == '2':
            state = self.xmi.makeActivityFinishState(name,self.activityModel)
        elif type == 'Script':
            state = self.xmi.makeActivityNodeState(name,self.activityModel)
            script = getElementText(self.ctx,'TWComponent/script',item)
            self.xmi.makeLocalTag('documentation',script,state)
        elif type == 'Switch':
            state = self.xmi.makeActivitySwitchState(name,self.activityModel)
        elif type == 'SubProcess' or type == '1' or impl == '1':
            state = self.xmi.makeActivityNodeState(name,self.activityModel)
            sid = state.prop('xmi.id')
            cref = getElementText(self.ctx,self.xpathImplID,item)
            cref = fixTwxRef(self.sid,cref)
            self.xmi.makeAssociation(name,None,None,self.diagramPackage,sid=sid,tid=cref)
        else:
            state = self.xmi.makeActivityNodeState(name,self.activityModel)

        if state == None:
            return None

        self.xmi.makeStereotype(type,state)
        self.pids[pid] = state

        layout = getElement(self.ctx,self.xpathLayout,item)
        if layout != None:
            geometry='Left=%d;Top=%d;Right=%d;Bottom=%d;'%(
                int(layout.prop('x')),
                offset+int(layout.prop('y')),
                int(layout.prop('x'))+10,
                offset+int(layout.prop('y'))+10,
            )
        else:
            geometry=None

        self.xmi.addDiagramState(state,self.activityDiagram,geometry=geometry)

        return state

    def exportAttribute(self,property):
        name = property.prop('name')
        cref = getElementText(self.ctx,'classId',property)
        direction = getElementText(self.ctx,'parameterType',property)
        cref = fixTwxRef(self.sid,cref)
        interface = self.params['private']
        if direction == '1':
            interface = self.params['input']
        if direction == '2':
            interface = self.params['output']
        uid = interface.parent.prop('xmi.id')
        array = getElementText(self.ctx,'isArrayOf',property) == 'true'
        self.xmi.makeAttribute(name,None,None,interface,tid=cref,array=array)
        self.xmi.makeAssociation(name,None,None,self.interfaces,sid=uid,tid=cref,array=array)
        
