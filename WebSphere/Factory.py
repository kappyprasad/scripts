#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import Types
import WebSphere

class Factory(WebSphere.Entity):
    
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self,description):
        self.__description = description
        return

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
        super(Factory,self).__init__(doc,ctx)
        self.__description = None
        self.__jndi = None
        return

    def __dir__(self):
        return super(Factory,self).__dir__() + [ 
            'description', 
            'jndi' 
        ]

    def process(self,element):
        self.description = '%s'%element.prop('description')
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('name')
        self.jndi = '%s'%element.prop('jndiName')
        self.documentation = '%s'%element
        return


    

