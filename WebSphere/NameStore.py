#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class NameStore(WebSphere.Entity):
    
    @property
    def contextID(self):
        return self.__contextID

    @contextID.setter
    def contextID(self,contextID):
        self.__contextID = contextID
        return

    @property
    def parentContextID(self):
        return self.__parentContextID

    @parentContextID.setter
    def parentContextID(self,parentContextID):
        self.__parentContextID = parentContextID
        return

    def __init__(self,doc=None,ctx=None):
        super(NameStore,self).__init__(doc,ctx)
        self.__contextID = None
        self.__parentContextID = None
        return

    def __dir__(self):
        return super(NameStore,self).__dir__() + [ 
            'parentContextID', 
            'contextID' 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        self.contextID = '%s'%element.prop('contextId')
        self.parentContextID = '%s'%element.prop('parentContextId')
        return


    

