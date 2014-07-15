#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



####################################################################################
import sys,re,os,uuid

from datetime import *

from _tools.xpath import *
from _tools.pretty import *

####################################################################################
def generateID():
    return 'EDDO_%s'%uuid.uuid4()

####################################################################################
class XMI:

    exporter  = '$HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/xmi.py $'
    version   = '$Revision: 11882 $'
    timestamp = '%Y-%m-%d %H:%M:%S'

    classDiagramStyle = {
        'ShowPrivate' : '1',
        'ShowProtected' : '1',
        'ShowPublic' : '1',
        'HideRelationships' : '0',
        'Locked' : '0',
        'Border' : '1',
        'HighlightForeign' : '1',
        'PackageContents' : '0',
        'SequenceNotes' : '0',
        'ScalePrintImage' : '1',
        'PPgs.cx' : '1',
        'PPgs.cy' : '1',
        'DocSize.cx' : '1000',
        'DocSize.cy' : '1000',
        'ShowDetails' : '0',
        'Orientation' : 'P',
        'Zoom' : '100',
        'ShowTags' : '0',
        'OpParams' : '1',
        'VisibleAttributeDetail' : '0',
        'ShowOpRetType' : '1',
        'ShowIcons' : '1',
        'CollabNums' : '1',
        'HideProps' : '1',
        'ShowReqs' : '0',
        'ShowCons' : '0',
        'PaperSize' : '1',
        'HideParents' : '1',
        'UseAlias' : '0',
        'HideAtts' : '0',
        'HideOps' : '0',
        'HideStereo' : '0',
        'HideElemStereo' : '0',
        'ShowTests' : '0',
        'ShowMaint' : '0',
        'ConnectorNotation' : 'UML 2.1',
        'ExplicitNavigability' : '0',
        'AdvancedElementProps' : '1',
        'AdvancedFeatureProps' : '1',
        'AdvancedConnectorProps' : '1',
        'ShowNotes' : '0',
        'SuppressBrackets' : '0',
        'SuppConnectorLabels' : '0',
        'PrintPageHeadFoot' : '0',
        'ShowAsList' : '0',
    }

    activityDiagramStyle = {
        'ShowPrivate':'1',
        'ShowProtected':'1',
        'ShowPublic':'1',
        'HideRelationships':'0',
        'Locked':'0',
        'Border':'1',
        'HighlightForeign':'1',
        'PackageContents':'1',
        'SequenceNotes':'0',
        'ScalePrintImage':'0',
        'PPgs.cx':'1',
        'PPgs.cy':'1',
        'DocSize.cx':'850',
        'DocSize.cy':'1098',
        'ShowDetails':'0',
        'Orientation':'P',
        'Zoom':'100',
        'ShowTags':'0',
        'OpParams':'1',
        'VisibleAttributeDetail':'0',
        'ShowOpRetType':'1',
        'ShowIcons':'1',
        'CollabNums':'0',
        'HideProps':'0',
        'ShowReqs':'0',
        'ShowCons':'0',
        'PaperSize':'1',
        'HideParents':'0',
        'UseAlias':'0',
        'HideAtts':'0',
        'HideOps':'0',
        'HideStereo':'0',
        'HideElemStereo':'0',
        'ShowTests':'0',
        'ShowMaint':'0',
        'ConnectorNotation':'UML 2.1',
        'ExplicitNavigability':'0',
        'AdvancedElementProps':'1',
        'AdvancedFeatureProps':'1',
        'AdvancedConnectorProps':'1',
        'ShowNotes':'0',
        'SuppressBrackets':'0',
        'SuppConnectorLabels':'0',
        'PrintPageHeadFoot':'0',
        'ShowAsList':'0',
    }

    namespaces = {
        'UML' : 'org.omg.xmi.namespace.UML'
    }    

    @property
    def doc(self):
        return self.doc

    @property
    def root(self):
        return self.root

    @property
    def modelNS(self):
        return self.modelNS

    @property
    def files(self):
        return self.files

    def __init__(self):
        self.now = datetime.now()
        self.makeDocument()
        self.makeModel()
        self.makeExtensions()
        self.stereotypes = {}
        return

    def makeDocument(self):
        (self.doc,self.ctx) = getContextFromString('<XMI/>')
        for prefix in self.namespaces.keys():
            self.ctx.xpathRegisterNs(prefix, self.namespaces[prefix])
        # version
        self.root = self.doc.getRootElement()
        for prefix in self.namespaces.keys():
            self.root.setProp('xmlns:%s'%prefix, self.namespaces[prefix])
        self.root.setProp('xmi.version','1.2')
        # timestamp
        self.root.setProp('timestamp',self.now.strftime(self.timestamp))
        # header
        header = addElement(self.doc,'XMI.header',self.root)
        # documentation
        doco = addElement(self.doc,'XMI.documentation',header)
        addElementText(self.doc,'XMI.exporter',self.exporter,doco)
        addElementText(self.doc,'XMI.exporterVersion',self.version,doco)
        # metamodel
        meta = addElement(self.doc,'XMI.metamodel',header)
        meta.setProp('xmi.name','UML')
        meta.setProp('xmi.version','1.4')
        return 

    def makeModel(self):
        self.content = addElement(self.doc,'XMI.content',self.root)
        model = addElement(self.doc,'UML:Model',self.content)
        model.setProp('isAbstract','false')
        model.setProp('isLeaf','false')
        model.setProp('isRoot','true')
        model.setProp('isSpecification','false')
        model.setProp('name',self.now.strftime(self.timestamp))
        model.setProp('visibility','public')
        model.setProp('xmi.id',generateID())
        self.modelNS = addElement(self.doc,'UML:Namespace.ownedElement',model)
        #self.rootClass = self.makeClass('EARootClass',self.modelNS)
        #self.rootClass.parent.setProp('isRoot','true')
        return

    def makeExtensions(self):
        self.extensions = addElement(self.doc,'XMI.extensions')
        self.extensions.setProp('xmi.extender','Enterprise Architect 2.5')
        self.files = addElement(self.doc,'EAModel.file',self.extensions)
        return

    def makePackage(self,name,parent):
        package = addElement(self.doc,'UML:Package',parent)
        package.setProp('isAbstract','false')
        package.setProp('isLeaf','false')
        package.setProp('isRoot','true')
        package.setProp('isSpecification','false')
        package.setProp('name',name)
        package.setProp('visibility','public')
        package.setProp('xmi.id',generateID())
        element = addElement(self.doc,'UML:Namespace.ownedElement',package)
        return element

    def getPackage(self,name,parent):
        package = getElement(self.ctx,'*[@name="%s"]'%name,parent)
        if package == None:
            package = self.makePackage(name,parent)
        return package

    def makeClass(self,name,parent,uid=None):
        if not uid: uid=generateID()
        clasz = addElement(self.doc,'UML:Class',parent)
        clasz.setProp('isAbstract','false')
        clasz.setProp('isLeaf','false')
        clasz.setProp('isRoot','true')
        clasz.setProp('isSpecification','false')
        clasz.setProp('name',name)
        clasz.setProp('visibility','public')
        clasz.setProp('xmi.id',uid)
        self.makeLocalTag('ea_eleType','element',clasz)
        classCF = addElement(self.doc,'UML:Classifier.feature',clasz)
        return classCF

    def makeAttribute(self,name,type,value,parent,tid=None,array=False):
        attribute = addElement(self.doc,'UML:Attribute', parent)
        attribute.setProp('name',name)
        attribute.setProp('visibility','private')
        if array:
            self.makeLocalTag('collection','true',attribute)
            self.makeLocalTag('container','[]',attribute)
        if type: 
            tid = type.parent.prop('xmi.id')
        if tid:
            sf = addElement(self.doc,'UML:StructuralFeature.type',attribute)
            classifier = addElement(self.doc,'UML:Classifier',sf)
            classifier.setProp('xmi.idref',tid)
        if value:
            av = addElement(self.doc,'UML:Attribute.initialValue',attribute)
            ue = addElement(self.doc,'UML:Expression',av)
            ue.setProp('body',value)
        return attribute

    def makeOperation(self,name,parameters,returns,parent,pids={},rid=None):
        operation = addElement(self.doc,'UML:Operation', parent)
        operation.setProp('name',name)
        operation.setProp('visibility','public')
        bf = addElement(self.doc,'UML:BehavioralFeature.parameter',operation)
        if parameters:
            pids = {}
            for p in parameters.keys():
                pids[p] = parameters[p].parent.prop('xmi.id')
        for p in pids.keys():
            self.makeParameter(p,None,'in',bf,tid=pids[p])
        self.makeParameter('return',returns,'return',bf,tid=rid)
        return

    def makeParameter(self,name,type,kind,parent,tid=None):
        if type:
            tid = type.parent.prop('xmi.id')
        if not tid:
            return
        parameterP = addElement(self.doc,'UML:Parameter',parent)
        parameterP.setProp('xmi.id',generateID())
        parameterP.setProp('name',name)
        parameterP.setProp('kind',kind)
        parameterT = addElement(self.doc,'UML:Parameter.type',parameterP)
        parameterC = addElement(self.doc,'UML:Class',parameterT)
        parameterC.setProp('xmi.idref',tid)
        return

    def makeAssociation(self,name,source,target,parent,sid=None,tid=None,array=False):
        if source:
            sid = source.parent.prop('xmi.id')
        if target:
            tid = target.parent.prop('xmi.id')
        association = addElement(self.doc,'UML:Association',parent)
        association.setProp('name',name)
        association.setProp('xmi.id',generateID())
        association.setProp('visibility','public')
        association.setProp('isAbstract','false')
        association.setProp('isLeaf','false')
        association.setProp('isRoot','false')
        # connect em
        connection = addElement(self.doc,'UML:Association.connection',association)
        # source
        sourceEnd = addElement(self.doc,'UML:AssociationEnd',connection)
        sourceEnd.setProp('aggregation','none')
        sourceEnd.setProp('isNavigable','false')
        sourceEnd.setProp('xmi.id',generateID())
        sourceParticipant = addElement(self.doc,'UML:AssociationEnd.participant',sourceEnd)
        sourceClass = addElement(self.doc,'UML:Class',sourceParticipant)
        sourceClass.setProp('xmi.idref',sid)
        #target
        targetEnd = addElement(self.doc,'UML:AssociationEnd',connection)
        targetEnd.setProp('aggregation','none')
        targetEnd.setProp('isNavigable','true')
        targetEnd.setProp('xmi.id',generateID())
        if array:
            targetEndMulti = addElement(self.doc,'UML:AssociationEnd.multiplicity',targetEnd)
            multi = addElement(self.doc,'UML:Multiplicity',targetEndMulti)
            multi.setProp('xmi.id',generateID())
            multiRangeP = addElement(self.doc,'UML:Multiplicity.range',multi)
            multiRangeC = addElement(self.doc,'UML:MultiplicityRange',multiRangeP)
            multiRangeC.setProp('xmi.id',generateID())
            multiRangeC.setProp('lower','0')
            multiRangeC.setProp('upper','-1')
        targetParticipant = addElement(self.doc,'UML:AssociationEnd.participant',targetEnd)
        targetClass = addElement(self.doc,'UML:Class',targetParticipant)
        targetClass.setProp('xmi.idref',tid)
        return

    def makeObject(self,name,type,parent):
        cr = addElement(self.doc,'UML:ClassifierRole',parent)
        cr.setProp('name',name)
        cr.setProp('visibility','public')
        cr.setProp('xmi.id',generateID())
        #cr.setProp('base',self.rootClass.parent.prop('xmi.id'))
        self.makeLocalTag('classifier',type.parent.prop('xmi.id'),cr)
        self.makeLocalTag('classname',type.parent.prop('name'),cr)
        self.makeLocalTag('ea_stype','Object',cr)
        return cr

    def makeComment(self,text,parent):
        return

    def makeEAFile(self,path,type,parent):
        flement = addElement(self.doc,'EAFile',self.files)
        flement.setProp('name',path)
        flement.setProp('type',type)
        flement.setProp('subject',parent.prop('xmi.id'))
        if type == 'Web Address':
            return
        if type == 'Local File':
            self.makeLocalTag('filesize', '%d'%os.path.getsize(path),flement)
            modified = datetime.fromtimestamp(os.path.getmtime(path))
            self.makeLocalTag('timestamp',modified.strftime(self.timestamp),flement)
        return

    def makeLocalTag(self,name,value,parent):
        tags = getElement(self.ctx,'*[contains(local-name(),"taggedValue")]',parent)
        if tags is None:
            tags = addElement(self.doc,'UML:ModelElement.taggedValue',parent)
        tag = addElement(self.doc,'UML:TaggedValue',tags)
        tag.setProp('tag',name)
        tag.setProp('value',value)
        return

    def makeContentTag(self,name,value,parent):
        tag = addElement(self.doc,'UML:TaggedValue',self.content)
        tag.setProp('xmi.id',generateID())
        tag.setProp('tag',name)
        tag.setProp('value',value)
        tag.setProp('modelElement',parent.parent.prop('xmi.id'))
        return

    def makeStereotype(self,name,parent):
        if not name in self.stereotypes.keys():
            ust = addElement(self.doc,'UML:Stereotype',self.modelNS)
            ust.setProp('name',name)
            ust.setProp('xmi.id',generateID())
            self.stereotypes[name] = ust
        mes = addElement(self.doc,'UML:ModelElement.stereotype',parent.parent)
        stereotype = addElement(self.doc,'UML:Stereotype',mes)
        stereotype.setProp('xmi.idref',self.stereotypes[name].prop('xmi.id'))
        return

    def makeActivityModel(self,name,parent):
        model = addElement(self.doc,'UML:ActivityGraph',parent)
        model.setProp('name',name)
        model.setProp('xmi.id',generateID())
        return model

    def makeTransition(self,source,target,parent,name=None):
        transitions = getElement(self.ctx,'*[contains(local-name(),"transitions")]',parent)
        if transitions is None:
            transitions = addElement(self.doc,'UML:StateMachine.transitions',parent)
        transition = addElement(self.doc,'UML:Transition',transitions)
        transition.setProp('xmi.id',generateID())
        if name != None:
            transition.setProp('name',name)

        sourceT = addElement(self.doc,'UML:Transition.source',transition)
        sourceS = addElement(self.doc,source.name,sourceT)
        sourceS.setProp('xmi.idref',source.prop('xmi.id'))

        targetT = addElement(self.doc,'UML:Transition.target',transition)
        targetS = addElement(self.doc,target.name,targetT)
        targetS.setProp('xmi.idref',target.prop('xmi.id'))

        return transition

    def makeActivitySwimLane(self,name,parent):
        partitions = getElement(self.ctx,'*[contains(local-name(),"partition")]',parent)
        if partitions is None:
            partitions = addElement(self.doc,'UML:ActivityGraph.partition',parent)
        partition = addElement(self.doc,'UML:Partition',partitions)
        partition.setProp('name',name)
        partition.setProp('xmi.id',generateID())
        return partition
        
    def addActivityToLane(self,state,parent):
        contents = getElement(self.ctx,'*[contains(local-name(),"contents")]',parent)
        if contents is None:
            contents = addElement(self.doc,'UML:Partition.contents',parent)
        content = addElement(self.doc,state.name,contents)
        content.setProp('xmi.idref',state.prop('xmi.id'))
        self.makeLocalTag('owner',parent.prop('xmi.id'),state)
        return content
        
    def makeActivityStartState(self,name,parent,kind=None):
        state = self.makeActivityState(name,'Pseudostate',parent)
        state.setProp('kind','initial')
        return state

    def makeActivityNodeState(self,name,parent):
        state = self.makeActivityState(name,'ActionState',parent)
        self.makeLocalTag('ea_stype','StateNode',state)
        return state

    def makeActivitySwitchState(self,name,parent):
        state = self.makeActivityState(name,'ActionState',parent)
        state.setProp('kind','branch')
        self.makeLocalTag('ea_stype','Decision',state)
        return state

    def makeActivityFinishState(self,name,parent,kind=None):
        state = self.makeActivityState(name,'FinalState',parent)
        return state

    def makeActivityState(self,name,type,parent):
        types = {
            'Pseudostate' : 'StateNode',
            'ActionState' : 'Action',
            'FinalState'  : 'Final'
        }
        if type not in types.keys():
            raise Exception('type=%s not in %s'%(type,types.keys()))

        top = getElement(self.ctx,'*[contains(local-name(),"top")]',parent)
        if top is None:
            top = addElement(self.doc,'UML:StateMachine.top',parent)

        cs = getElement(self.ctx,'*[contains(local-name(),"CompositeState")]',top)
        if cs is None:
            cs = addElement(self.doc,'UML:CompositeState',top)
            cs.setProp('name','top')
            cs.setProp('xmi.id',generateID())

        sub = getElement(self.ctx,'*[contains(local-name(),"subvertex")]',cs)
        if sub is None:
            sub = addElement(self.doc,'UML:CompositeState.subvertex',cs)

        state = addElement(self.doc,'UML:%s'%type,sub)
        state.setProp('name',name)
        state.setProp('xmi.id',generateID())

        return state

    def makeClassDiagram(self,name,parent):
        diagram = self.makeDiagram(name,parent)
        diagram.parent.setProp('diagramType','ClassDiagram')
        self.makeLocalTag('type','Logical',diagram.parent)
        self.makeLocalTag('EAStyle',self.makeStyle(self.classDiagramStyle),diagram.parent)
        #self.makeLocalTag('styleex','SaveTag=6B7A16D7;ExcludeRTF=0;DocAll=0;HideQuals=0;AttPkg=1;ShowTests=0;ShowMaint=0;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;MatrixLineWidth=1;MatrixLocked=0;TConnectorNotation=UML 2.1;TExplicitNavigability=0;AdvancedElementProps=1;AdvancedFeatureProps=1;AdvancedConnectorProps=1;ProfileData=;MDGDgm=;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;ShowOpRetType=1;SuppressBrackets=0;SuppConnectorLabels=0;PrintPageHeadFoot=0;ShowAsList=0;SuppressedCompartments=;',diagram)
        return diagram

    def makeActivityDiagram(self,name,parent):
        diagram = self.makeDiagram(name,parent)
        diagram.parent.setProp('diagramType','ActivityDiagram')
        self.makeLocalTag('type','Activity',diagram.parent)
        self.makeLocalTag('EAStyle',self.makeStyle(self.activityDiagramStyle),diagram.parent)
        return diagram

    def makeDiagram(self,name,parent):
        diagram = addElement(self.doc,'UML:Diagram',self.content)
        diagram.setProp('name',name)
        diagram.setProp('toolName','Enterprise Architect 2.5')
        diagram.setProp('xmi.id',generateID())
        diagram.setProp('owner',parent.parent.prop('xmi.id'))
        self.makeLocalTag('package',parent.parent.prop('xmi.id'),diagram)
        elements = addElement(self.doc,'UML:Diagram.element',diagram)
        return elements

    def addDiagramClass(self,element,parent,geometry=None,style=None):
        self.addDiagramElement(element.parent,parent,geometry,style)

    def addDiagramState(self,element,parent,geometry=None,style=None):
        self.addDiagramElement(element,parent,geometry,style)
        
    def addDiagramElement(self,element,parent,geometry=None,style=None):
        child = addElement(self.doc,'UML:DiagramElement',parent)
        child.setProp('subject',element.prop('xmi.id'))
        if geometry != None:
            child.setProp('geometry',geometry)
        if style != None:
            child.setProp('style',style)
        return child

    def makeStyle(self,types):
        style = ''.join(
            map(
                lambda x : '%s=%s;'%(
                    x,types[x]
                )
                ,types.keys()
            )
        )
        return style



####################################################################################
