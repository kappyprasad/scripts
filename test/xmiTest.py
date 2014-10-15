#!/usr/bin/python

# $Date: 2014-06-24 18:48:37 +1000 (Tue, 24 Jun 2014) $
# $Revision: 11882 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/test/xmiTest.py $
# $Id: xmiTest.py 11882 2014-06-24 08:48:37Z david.edson $


import os,re,sys
import unittest, uuid

from _tools.test import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.xmi import *

class XMI_Test(unittest.TestCase):
    """xmi module test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_Build_Class_XMI(self):
        """build an XMI package with a set of classes."""
        xmi = XMI()

        # make the classes and class diagram

        classes = xmi.makePackage('Classes',xmi.modelNS)

        string = xmi.makeClass('String',classes)
        parent = xmi.makeClass('Parent',classes)
        child = xmi.makeClass('Child',classes)

        xmi.makeAttribute('names',string,None,child,array=True)
        xmi.makeAssociation('names',child,string,classes,array=True)

        xmi.makeAttribute('child',child,None,parent)
        xmi.makeAssociation('child',parent,child,classes)

        parameters = {
            'name' : string,
            'child' : child
        }
        returns=child
        xmi.makeOperation('getChild',parameters,returns,parent)

        xmi.makeStereotype('hifi',string)

        diagram = xmi.makeClassDiagram('Diagram',classes)
        xmi.addDiagramClass(parent,diagram)
        xmi.addDiagramClass(child,diagram)
        xmi.addDiagramClass(string,diagram)

        # export the results

        output=open('ClassDiagram.xmi','w')
        input = StringIO.StringIO('%s\n'%xmi.doc)
        doParse(False,False,True,input,False,output,False,True)
        input.close()
        output.close()

        return

    def test_02_Build_ActivityDiagram_XMI(self):
        """build an XMI package with a set of classes."""
        xmi = XMI()

        # make the actiities and actiity diagram

        activities    = xmi.makePackage('Activities',xmi.modelNS)
        activityModel = xmi.makeActivityModel('Activities',activities)
        underLane     = xmi.makeActivitySwimLane('Under',activityModel)
        overLane      = xmi.makeActivitySwimLane('Over',activityModel)

        startState  = xmi.makeActivityStartState('Start',activityModel)
        lowerState  = xmi.makeActivityNodeState('Lower',activityModel)
        upperState  = xmi.makeActivityNodeState('Upper',activityModel)
        finishState = xmi.makeActivityFinishState('Finish',activityModel)

        xmi.addActivityToLane(startState,underLane)
        xmi.addActivityToLane(lowerState,underLane)
        xmi.addActivityToLane(upperState,overLane)
        xmi.addActivityToLane(finishState,overLane)

        startToLower  = xmi.makeTransition(startState,lowerState,activityModel)
        lowerToUpper  = xmi.makeTransition(lowerState,upperState,activityModel)
        upperToFinish = xmi.makeTransition(upperState,finishState,activityModel)

        diagram = xmi.makeActivityDiagram('Activities',activities)
        xmi.addDiagramState(underLane,diagram,geometry='Left=42;Top=33;Right=830;Bottom=208;',style='Dockable=on;')
        xmi.addDiagramState(overLane,diagram,geometry='Left=42;Top=208;Right=830;Bottom=383;',style='Dockable=on;')
        xmi.addDiagramState(startState,diagram,geometry='Left=98;Top=285;Right=118;Bottom=305;')
        xmi.addDiagramState(lowerState,diagram,geometry='Left=226;Top=261;Right=361;Bottom=336;')
        xmi.addDiagramState(upperState,diagram,geometry='Left=454;Top=81;Right=589;Bottom=156;')
        xmi.addDiagramState(finishState,diagram,geometry='Left=740;Top=288;Right=760;Bottom=308;')

        xmi.addDiagramElement(startToLower,diagram,style='TREE=H')
        xmi.addDiagramElement(lowerToUpper,diagram,style='TREE=H')
        xmi.addDiagramElement(upperToFinish,diagram,style='TREE=H')
        # export the results

        output=open('ActivityDiagram.xmi','w')
        input = StringIO.StringIO('%s\n'%xmi.doc)
        doParse(False,False,True,input,False,output,False,True)
        input.close()
        output.close()

        return

if __name__ == '__main__':
    unittest.main()
