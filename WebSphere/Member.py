#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Member(WebSphere.Entity):
    
    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self,value):
        self.__node.value = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self,value):
        self.__weight = value

    def __init__(self, doc=None,ctx=None,element=None):
        super(Member,self).__init__(doc,ctx)
        self.element = element
        self.__node = Types.Typed(WebSphere.Node)
        self.__weight = 1
        return

    def __dir__(self):
        return super(Member,self).__dir__() + [ 
            'node',
            'weight' 
        ]

    def process(self):
        self.id = '%s'%self.element.prop('uniqueId')
        self.name = '%s'%self.element.prop('memberName')
        self.weight = '%s'%self.element.prop('weight')
        # have to do Node
        return

