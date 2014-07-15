#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types

class Entity(Types.Object):

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,id):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def documentation(self):
        return self.__documentation

    @documentation.setter
    def documentation(self,documentation):
        self.__documentation = documentation

    def __init__(self,doc=None,ctx=None):
        (self.doc,self.ctx) = (doc,ctx)
        self.__id = None
        self.__name = None
        self.__documentation = None
        return

    def __dir__(self):
        return [ 
            'id', 
            'name', 
        ]

    def process(self,xpath):
        node = getElement(self.ctx,xpath)
        if node == None:
            return
        self.id = '%s'%node.prop('id')
        self.name = '%s'%node.prop('name')
    
    def export(self,xmi,parent):
        clasz = xmi.makeClass(self.name,parent)
        for key in dir(self):
            obj = getattr(self,key)
            xmi.makeAttribute(key,None,'%s'%obj,clasz)
        if self.documentation != None:
            xmi.makeLocalTag('documentation','%s'%self.documentation,clasz.parent)
        return clasz

