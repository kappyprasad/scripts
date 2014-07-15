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

####################################################################################
def concatPath(prefix,suffix):
    path = suffix
    if prefix:
        path = '%s/%s'%(prefix.rstrip('/'),suffix)
    return path

####################################################################################
class Tree:

    resources = {
        'JDBCProvider'       : 'resources.jdbc:JDBCProvider',
        'JMSProvider'        : 'resources.jms:JMSProvider',
        'MailProvider'       : 'resources.mail:MailProvider',
        'URLProvider'        : 'resources.url:URLProvider',
        'J2CResourceAdapter' : 'resources.j2c:J2CResourceAdapter',
    }

    @property
    def doc(self):
        return self.xmi.doc

    def __init__(self,xmi=XMI(),verbose=False):
        self.xmi = xmi
        self.types = {}
        self.verbose = verbose

    def processTypes(self):
        types = self.xmi.makePackage('Types', self.xmi.modelNS)
        # fundamentals
        self.types['String']   = self.xmi.makeClass('String',types)
        self.types['Boolean']  = self.xmi.makeClass('Boolean',types)
        self.types['Integer']  = self.xmi.makeClass('Integer',types)
        self.types['Date']     = self.xmi.makeClass('Date',types)
        #websphere variable
        self.types['Variable'] = self.xmi.makeClass('Variable',types)
        self.xmi.makeAttribute('symbolicName',self.types['String'], self.types['Variable'])
        self.xmi.makeAttribute('description', self.types['String'], self.types['Variable'])
        self.xmi.makeAttribute('value',       self.types['String'], self.types['Variable'])
        return

    def processDirectory(self,name,parent=None,prefix=None):
        if parent == None:
            parent = self.xmi.modelNS
        parent = self.xmi.makePackage(name,parent)
        dir = concatPath(prefix,name)
        for f in os.listdir(dir):
            fp = concatPath(dir,f)
            if self.verbose:
                sys.stderr.write('< %s\n'%fp)
                sys.stderr.flush()
            if os.path.isfile(fp):
                self.processFile(f,parent,dir)
            if os.path.isdir(fp):
                self.processDirectory(f,parent,dir)
        return

    def processFile(self,name,parent,prefix=None):
        (doc,ctx)=getContextFromFile(concatPath(prefix,name))
        target = None
        child = None

        if name == 'cell.xml':
            #parent = self.xmi.getPackage('Cells',parent)
            cell = getElement(ctx,'/topology.cell:Cell')
            if cell: target = cell.prop('name')
            child = 'nodes/'

        if name == 'node.xml':
            #parent = self.xmi.getPackage('Nodes',parent)
            node = getElement(ctx,'/topology.node:Node')
            if node: target = node.prop('name')
            child = 'servers/'

        if name == 'server.xml':
            #parent = self.xmi.getPackage('Servers',parent)
            server = getElement(ctx,'/process:Server')
            if server: target = server.prop('name')

        if name == 'cluster.xml':
            package = self.xmi.getPackage('Clusters',parent)
            for entry in getElements(ctx,'/topology.cluster:ServerCluster/members'):
                cluster = self.xmi.makeClass(entry.prop('memberName'),package)
                for name in ['nodeName','weight']:
                    self.xmi.makeAttribute(name,None,entry.prop(name),cluster)
                    self.xmi.makeContentTag(name,entry.prop(name),cluster)

        if name == 'variables.xml':
            package = self.xmi.getPackage('Variables',parent)
            for entry in getElements(ctx,'/variables:VariableMap/entries'):
                variable = self.xmi.makeClass(entry.prop('symbolicName'),package)
                for name in ['description','value']:
                    self.xmi.makeAttribute(name,None,entry.prop(name),variable)
                    self.xmi.makeContentTag(name,entry.prop(name),variable)
        
        if name == 'namestore.xml':
            package = self.xmi.getPackage('NameStore',parent)
            for entry in getElements(ctx,'/xmi:XMI/namestore:NamingContext'):
                namestore = self.xmi.makeClass(entry.prop('contextId'),package)
                for name in ['parentContextId']:
                    self.xmi.makeAttribute(name,None,entry.prop(name),namestore)
                    self.xmi.makeContentTag(name,entry.prop(name),namestore)
        
        if name == 'libraries.xml':
            package = self.xmi.getPackage('Libraries',parent)
            for entry in getElements(ctx,'/xmi:XMI/libraries:Library'):
                library = self.xmi.makeClass(entry.prop('name'),package)
        
        if name == 'serverindex.xml':
            package = self.xmi.getPackage('Applications',parent)
            for entry in getElements(ctx,'/serverindex:ServerIndex/serverEntries'):
                server = self.xmi.getPackage(entry.prop('serverName'),package)
                for entry in getElements(ctx,'deployedApplications',entry):
                    application = self.xmi.makeClass(entry.content,server)
        
        if name == 'resources.xml':
            for resource in self.resources.keys():
                package = self.xmi.getPackage(resource,parent)
                try:
                    for entry in getElements(ctx,'/xmi:XMI/%s'%self.resources[resource]):
                        jdbcProvider = self.xmi.makeClass(entry.prop('name'),package)
                        for property in entry.properties:
                            if property.type == 'attribute' and property.name != 'xmi.id':
                                name = property.name
                                self.xmi.makeAttribute(name,None,entry.prop(name),jdbcProvider)
                                self.xmi.makeContentTag(name,entry.prop(name),jdbcProvider)
                except:
                    None
            for resource in ['factories','j2cAdminObjects','j2cActivationSpec']:
                package = self.xmi.getPackage(resource,parent)
                try:
                    for entry in getElements(ctx,'//%s'%resource):
                        jndi = self.xmi.makeClass(entry.prop('jndiName'),package)
                        for property in entry.properties:
                            if property.type == 'attribute' and property.name != 'xmi.id':
                                name = property.name
                                self.xmi.makeAttribute(name,None,entry.prop(name),jndi)
                                self.xmi.makeContentTag(name,entry.prop(name),jndi)
                except:
                    None


        del (doc,ctx)

        return
