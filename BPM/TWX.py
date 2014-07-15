#!/usr/bin/python

# $Date: 2014-06-24 18:04:17 +1000 (Tue, 24 Jun 2014) $
# $Revision: 11881 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/BPM/TWX.py $
# $Id: TWX.py 11881 2014-06-24 08:04:17Z david.edson $


import sys, re, os, urllib, urllib2, StringIO
import argparse

from _tools.xmi import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.finder import *
from _tools.eddo import *

from utils import *
from TWClass import TWClass
from TWProcess import TWProcess
from TWService import TWService
from TWBPD import TWBPD

####################################################################################
class TWX:

    tab='\t'
    horizon = buildHorizon()

    cp  = re.compile('^.*\s(\S+\.class)$')
    jar = re.compile('^.*\.jar$')
    fn  = re.compile('.*(function).*')

    @property
    def doc(self):
        return self.xmi.doc

    @property
    def project(self):
        return self.project

    @property
    def toolkits(self):
        return self.toolkits

    @property
    def objects(self):
        return self.objects

    @property
    def types(self):
        return self.types

    @property
    def classes(self):
        return self.classes

    @property
    def claszes(self):
        return self.claszes

    @property
    def assets(self):
        return self.assets

    @property
    def files(self):
        return self.files

    def __init__(self, colour=False, verbose=False, output=sys.stderr):
        self.verbose = verbose
        self.output = output
        self.colour = colour
        self.colours = getColours(html=False)
        if not self.colour:
            for key in self.colours.keys():
                self.colours[key] = ''
        self.project = {}
        self.toolkits = {}
        self.objects = {}
        self.assets = {}
        self.files = {}
        return

    def processFolder(self, dir):
        self.dependencies = {}
        for d in findFiles(dir,False,'^.*\.twx\.exploded$'):
            sys.stderr.write('%s\n'%self.horizon)
            twx = TWX(verbose=self.verbose,colour=self.colour)
            twx.processApplication(d,None,self.dependencies)
            key = '%s/%s'%(twx.project['name'],twx.project['sname'])
            #sys.stderr.write('fkey=%s\n'%key)
            if key not in self.dependencies.keys():
                self.dependencies[key] = twx
        return

    def processApplication(self, appdir, toolkitdir=None,dependencies=None):
        if toolkitdir:
            color = self.colours['Green']
            d=toolkitdir
        else:
            color = self.colours['Purple'] 
            d=appdir

        self.getPackage(d)

        if dependencies == None: 
            key = '%s/%s'%(self.project['name'],self.project['sname'])
            #sys.stderr.write('akey=%s\n'%key)
            dependencies = { key : self }
        self.dependencies = dependencies

        self.output.write('%s%s%s (%s)\n'%(color,self.project['name'],self.colours['Off'],self.project['sname']))
        self.output.flush()

        self.types = {}
        self.claszes = {}

        for key in self.objects.keys():
            self.getTypes('%s/objects/%s.xml'%(d,key))

        if self.verbose:
            self.printTypes()

        self.processClasses(d, toolkitdir)
        self.processFiles(d, toolkitdir)

        self.output.write('\n')
        self.output.flush()

        for pname in self.toolkits.keys():
            (did,sid,sname) = self.toolkits[pname]
            dids[did] = sid
            key = '%s/%s'%(pname,sname)
            #sys.stderr.write('tkey=%s\n'%key)
            if key not in self.dependencies.keys():
                p = '%s/toolkits/%s.zip.exploded'%(appdir,sid)
                self.dependencies[key] = TWX(verbose=self.verbose,colour=self.colour)
                self.dependencies[key].processApplication(appdir, p, self.dependencies)

        return

    def processClasses(self, d, toolkitdir):
        self.classes = {}

        if not os.path.isdir('%s/files'%d):
            return

        for i in self.files.keys():
            name = self.assets[i]
            path = self.files[i]
            f = '%s/files/%s/%s.jar.log'%(d,i,path)
            if not self.jar.match(name):
                continue
            if not os.path.isfile('%s'%f):
                 continue

        if len(self.classes) > 0:
            self.output.write('%s%sclasses ...%s\n'%(self.tab*1,self.colours['Teal'],self.colours['Off']))
            self.output.flush()
            for clasz in self.classes.keys():
                classes = self.classes[clasz]
                if self.verbose:
                    self.output.write('%s%s%s%s\n'%(self.tab*2,self.colours['Orange'],clasz,self.colours['Off']))
                    self.output.flush()
                    for clasz in classes:
                        self.output.write('%s%s\n'%(self.tab*3,clasz))

        return

    def processFiles(self, d, toolkitdir):
        ascii = {}
        if not os.path.isdir('%s/files'%d):
            return

        for i in self.files.keys():
            name = self.assets[i]
            path = self.files[i]
            f = '%s/files/%s/%s.txt'%(d,i,path)
            if self.jar.match(name):
                continue
            if not os.path.isfile('%s'%f):
                 continue

            founds = []

            if len(founds) > 0:
                ascii[name] = founds

        if len(ascii) > 0:
            self.output.write('%s%sfiles ...%s\n'%(self.tab*1,self.colours['Teal'],self.colours['Off']))
            self.output.flush()
            for key in ascii.keys():
                founds = ascii[key]
                if len(founds) > 0:
                    self.output.write('%s%s%s%s\n'%(self.tab*2,self.colours['Orange'],key,self.colours['Off']))
                    self.output.flush()
                    for found in founds:
                        self.output.write('%s%s\n'%(self.tab*3,found))

        return

    def getPackage(self,path):
        fp = '%s/META-INF/package.xml'%path
        #if not os.access(fp,os.F_OK): 
        #    return (None, None, None)

        (package,context) = getContextFromFile(fp)

        
        self.project['name'] = getElementText(context,'/p:package/target/project/@name')
        self.project['sid']  = getElementText(context,'/p:package/target/snapshot/@id')
        self.project['sname'] = getElementText(context,'/p:package/target/snapshot/@name')

        for dependency in getElements(context,'/p:package/dependencies/dependency'):
            did = dependency.prop('id').split('.')[1]
            isSystem = getElementText(context,'project/@isSystem',dependency)
            pname = getElementText(context,'project/@name',dependency)
            vname = getElementText(context,'snapshot/@id',dependency)
            sname = getElementText(context,'snapshot/@name',dependency)
            self.toolkits[pname] = (did,vname,sname)

        for objekt in getElements(context,'/p:package/objects/object'):
            if objekt.prop('type') == 'managedAsset':
                self.assets[objekt.prop('id')] = objekt.prop('name')
            else:
                self.objects[objekt.prop('id')] = objekt.prop('name')

        for fe in getElements(context,'p:package/files/file'):
            self.files[fe.prop('id')] = fe.prop('path')

        return

    def getSchema(self,variable, version):
        url = 'http://%s:%s/webapi/ViewSchema.jsp?type=%s&version=%s'%(
            host, port, variable, version
        )
        response = urllib2.urlopen(url)
        xsd = response.read()
        response.close()
        return xsd

    def getTypes(self,file):
        (doc,ctx) = getContextFromFile(file)
        element = getElement(ctx,'/teamworks/*')
        tipe = element.name
        if tipe not in self.types.keys():
            self.types[tipe] = {}
        name = element.prop('name')
        self.types[tipe][name] = (doc,ctx)
        return

    def printTypes(self):
        count = 0
        for tipe in self.types.keys():
            count += len(self.types[tipe])

        if count == 0:
            return

        for tipe in self.types.keys():
            tname = tipe.replace('process','service')
            self.output.write('%s%s%s ...%s\n'%(self.tab*1,self.colours['Teal'],tname,self.colours['Off']))
            self.output.flush()

            if self.verbose:
                names = self.types[tipe]
                for name in names.keys():
                    self.output.write ('%s%s%-50s%s\n'%(self.tab*2,self.colours['Orange'],name,self.colours['Off']))
                    self.output.flush()

        return

    def processExport(self,parent):

        packages = {
#            appName : ( 
#                package,  {
#                    snapName : (
#                        package, {
#                            typeName : (
#                                package, {
#                                    uid : xmi.id
#                                }
#                            )
#                        }
#                    )
#                } 
#            )
        }
        
        for key in sorted(self.dependencies.keys()):
            application = self.dependencies[key]
            sid = application.project['sid']

            appname = application.project['name']
            if not appname in packages.keys():
                packages[appname] = (self.xmi.makePackage(appname,parent),{})
            (package,versions) = packages[appname]
            
            vername = application.project['sname']
            if not vername in versions.keys():
                versions[vername] = (self.xmi.makePackage(vername,package),{})
            (version,types) = versions[vername]

            interfaces = self.xmi.makePackage('interfaces',version)

            sys.stdout.write('%s (%s)\n'%(appname,vername))

            for type in application.types.keys():
                if not type in types.keys():
                    package = self.xmi.makePackage(type,version)
                    diagram = self.xmi.makeClassDiagram(type,package)
                    types[type] = (package,diagram)
                (typePackage,diagram) = types[type]

                if type == 'twClass':
                    for clasz in application.types[type].keys():
                        (doc,ctx) = application.types[type][clasz]
                        helper = TWClass(self.xmi,doc,ctx,sid,typePackage)
                        twClass = helper.exportClasz(type,clasz)
                        self.xmi.addDiagramClass(twClass,diagram)

                elif type == 'process':
                    for clasz in application.types[type].keys():
                        (doc,ctx) = application.types[type][clasz]
                        helper = TWService(self.xmi,doc,ctx,sid,typePackage,interfaces)
                        twService = helper.exportProcess(clasz)
                        self.xmi.addDiagramClass(twService,diagram)
                        
                elif type == 'bpd':
                    for clasz in application.types[type].keys():
                        (doc,ctx) = application.types[type][clasz]
                        helper = TWBPD(self.xmi,doc,ctx,sid,typePackage,interfaces)
                        twBPD = helper.exportProcess(clasz)
                        self.xmi.addDiagramClass(twBPD,diagram)

                else:
                    for clasz in application.types[type].keys():
                        (doc,ctx) = application.types[type][clasz]
                        # make seperate class
                        cid = getElement(ctx,'/teamworks/*').prop('id')
                        uid = fixTwxID(sid,cid)
                        twClass = self.xmi.makeClass(clasz,typePackage,uid=uid)
                        #self.xmi.makeContentTag('xmi.id',cid,twClass)
                        self.xmi.makeStereotype(type,twClass)
                        self.xmi.addDiagramClass(twClass,diagram)
        return

    def exportXMI(self):
        sys.stderr.write('%s\n'%self.horizon)
        self.xmi = XMI()
        self.processExport(self.xmi.modelNS)
        if self.verbose:
            sys.stderr.write('%s\ndependency id->sid\n'%self.horizon)
            prettyPrint(dids)
        return self.xmi.doc;

