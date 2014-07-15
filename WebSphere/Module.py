#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$



from _tools.xpath import *

import Types
import WebSphere

class Module(WebSphere.Entity):

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,type):
        self.__type = type
        return

    def __init__(self,doc=None,ctx=None):
        super(Module,self).__init__(doc,ctx)
        self.type = None
        return

    def __dir__(self):
        return super(Module,self).__dir__() + [ 
            'type', 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        child  = getElement(self.ctx,'*',element)
        self.type = child.name
        if self.type == 'web':
            self.name = getElementText(self.ctx,'web-uri',child)
        elif self.type == 'ejb':
            self.name = child.content
        self.documentation = '%s'%element
        return

        
