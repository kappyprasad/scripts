#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Library(WebSphere.Package):
    
    @property
    def isolated(self):
        return self.__isolated

    @isolated.setter
    def isolated(self,isolated):
        self.__isolated = isolated
        return

    @property
    def classPaths(self):
        return self.__classPaths

    def __init__(self,doc=None,ctx=None):
        super(Library,self).__init__(doc,ctx)
        self.__classPaths = Types.List(str)
        return

    def __dir__(self):
        return super(Library,self).__dir__() + [ 
            'classPaths', 
            'isolated' 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('name')
        self.isolated = '%s'%element.prop('isolatedClassLoader')
        for cp in getElements(self.ctx,'classPath',element):
            self.classPaths.append('%s'%cp.content)
        return

    

