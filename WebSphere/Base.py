#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Base(WebSphere.Package):
    
    @property
    def resources(self):
        return self.__resources

    @property
    def variables(self):
        return self.__variables

    @property
    def libraries(self):
        return self.__libraries

    @property
    def nameStores(self):
        return self.__nameStores

    @property
    def nameBindings(self):
        return self.__nameBindings

    def __init__(self, doc=None,ctx=None):
        super(Base,self).__init__(doc,ctx)
        self.__resources    = Types.Map('name',WebSphere.Resource)
        self.__variables    = Types.Map('name',WebSphere.Variable)
        self.__libraries    = Types.Map('name',WebSphere.Library)
        self.__nameStores   = Types.Map('name',WebSphere.NameStore)
        self.__nameBindings = Types.Map('name',WebSphere.NameBinding)
        return

    def __dir__(self):
        return super(Base,self).__dir__() + [ 
            'resources',
            'variables', 
            'libraries',
            'nameStores',
            'nameBindings',
        ]

