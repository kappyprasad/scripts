#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




import sys,re,os,argparse,StringIO

from _tools.xmi import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.finder import *
from _tools.eddo import *

import Types
import WebSphere

horizon = buildHorizon()

####################################################################################
def concatPath(prefix,suffix):
    path = suffix
    if prefix:
        path = '%s/%s'%(prefix.rstrip('/'),suffix)
    return path

####################################################################################
class Tree(Types.Object):

    @property
    def cells(self):
        return self.__cells

    def __init__(self,verbose=False):
        self.verbose = verbose
        self.xmi = XMI()
        self.__cells = Types.Map('name',WebSphere.Cell)
        self.scope = None
        return

    def __dir__(self):
        return [ 'cells' ]

    def processDirectory(self,name,prefix=None):
        dir = concatPath(prefix,name)

        for f in os.listdir(dir):
            fp = concatPath(dir,f)
            if os.path.isfile(fp):
                try:
                    self.processFile(f,dir)
                except (libxml2.xpathError):
                    None

        for f in os.listdir(dir):
            fp = concatPath(dir,f)
            if os.path.isdir(fp):
                self.processDirectory(f,dir)

        return

    def processFile(self,name,prefix=None):
        (doc,ctx)=getContextFromFile(concatPath(prefix,name))

        target = None
        child = None

        if name == 'cell.xml':
            self.cell = WebSphere.Cell(doc,ctx)
            self.cell.process()
            self.cells.append(self.cell)
            self.scope = self.cell

        if name == 'cluster.xml':
            self.cluster = WebSphere.Cluster(doc,ctx)
            self.cluster.process()
            self.cell.clusters.append(self.cluster)
            self.scope = self.cluster

        if name == 'node.xml':
            self.node = WebSphere.Node(doc,ctx)
            self.node.process()
            self.cell.nodes.append(self.node)
            self.scope = self.node

        if name == 'server.xml':
            self.server = WebSphere.Server(doc,ctx)
            self.server.process()
            self.node.servers.append(self.server)
            self.scope = self.server

        if name == 'libraries.xml':
            for entry in getElements(ctx,'/xmi:XMI/libraries:Library'):
                library = WebSphere.Library(doc,ctx)
                library.process(entry)
                if self.scope != None and isinstance(self.scope,WebSphere.Base):
                    self.scope.libraries.append(library)
        
        if name == 'variables.xml':
            for entry in getElements(ctx,'/variables:VariableMap/entries'):
                variable = WebSphere.Variable(doc,ctx)
                variable.process(entry)
                if self.scope != None and isinstance(self.scope,WebSphere.Base):
                    self.scope.variables.append(variable)
                
        if name == 'namestore.xml':
            for entry in getElements(ctx,'/xmi:XMI/namestoxre:NamingContext'):
                nameStore = WebSphere.NameStore(doc,ctx)
                nameStore.process(entry)
                if self.scope != None and isinstance(self.scope,WebSphere.Base):
                    self.scope.nameStores.append(nameStore)

        if name == 'namebindings.xml':
            for entry in getElements(ctx,'xmi:XMI/namebindings:StringNameSpaceBinding'):
                nameBinding = WebSphere.NameBinding(doc,ctx)
                nameBinding.process(entry)
                if self.scope != None and isinstance(self.scope,WebSphere.Base):
                    self.scope.nameBindings.append(nameBinding)

        if name == 'serverindex.xml':
            for entry in getElements(ctx,'/serverindex:ServerIndex/serverEntries'):
                serverIndex = WebSphere.ServerIndex(doc,ctx)
                serverIndex.process(entry)
                if self.scope != None and isinstance(self.scope,WebSphere.Node):
                    self.scope.serverIndexes.append(serverIndex)
        
        if name == 'application.xml':
            application = WebSphere.Application(doc,ctx)
            application.process()
            if self.scope != None and isinstance(self.scope,WebSphere.Cell):
                self.scope.applications.append(application)

        if name == 'deployment.xml':
            None

        if name == 'resources.xml':
            resources = WebSphere.Resource.resources
            for resource in resources.keys():
                try:
                    for entry in getElements(ctx,'/xmi:XMI/%s'%resources[resource]):
                        resource = WebSphere.Resource(doc,ctx)
                        resource.process(entry)
                        if self.scope != None and isinstance(self.scope,WebSphere.Base):
                            self.scope.resources.append(resource)
                except (libxml2.xpathError):
                    None

        del (doc,ctx)

        return

    def export(self):
        package = self.xmi.makePackage('Cells',self.xmi.modelNS)
        diagram = self.xmi.makeClassDiagram('Cells',package)
        for cell in self.cells:
            pkg = cell.export(self.xmi,package)
            if pkg != None:
                self.xmi.addDiagramClass(pkg,diagram)
        # link associations
        return self.xmi.doc

        
        
