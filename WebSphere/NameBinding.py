#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import Types
import WebSphere

class NameBinding(WebSphere.Entity):
    
    @property
    def jndi(self):
        return self.__jndi

    @jndi.setter
    def jndi(self,jndi):
        self.__jndi = jndi
        return

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self,value):
        self.__value = value
        return

    def __init__(self,doc=None,ctx=None):
        super(NameBinding,self).__init__(doc,ctx)
        self.__value = None
        self.__jndi = None
        return

    def __dir__(self):
        return super(NameBinding,self).__dir__() + [ 
            'value', 
            'jndi' 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('name')
        self.value = '%s'%element.prop('stringToBind')
        self.jndi = '%s'%element.prop('nameInNameSpace')
        return

    

