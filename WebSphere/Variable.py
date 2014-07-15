#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


import WebSphere

class Variable(WebSphere.Entity):
    
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self,description):
        self.__description = description
        return

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self,value):
        self.__value = value
        return

    def __init__(self,doc=None,ctx=None):
        super(Variable,self).__init__(doc,ctx)
        self.__value = None
        return

    def __dir__(self):
        return super(Variable,self).__dir__() + [ 
            'value', 
            'description' 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('symbolicName')
        self.value = '%s'%element.prop('value')
        self.description = '%s'%element.prop('description')
        return


    

