#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Resource(WebSphere.Package):

    resources = {
        'JDBCProvider'       : 'resources.jdbc:JDBCProvider',
        'JMSProvider'        : 'resources.jms:JMSProvider',
        'MailProvider'       : 'resources.mail:MailProvider',
        'URLProvider'        : 'resources.url:URLProvider',
        'J2CResourceAdapter' : 'resources.j2c:J2CResourceAdapter',
    }

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self,description):
        self.__description = description
        return

    @property
    def clasz(self):
        return self.__clasz

    @clasz.setter
    def clasz(self,clasz):
        self.__clasz = clasz
        return

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self,category):
        self.__category = category
        return

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,type):
        self.__type = type
        return

    @property
    def factories(self):
        return self.__factories

    def __init__(self, doc=None,ctx=None):
        super(Resource,self).__init__(doc,ctx)
        self.__description = None
        self.__clasz = None
        self.__category = None
        self.__type = None
        self.__factories = Types.Map('name',WebSphere.Factory)
        return

    def __dir__(self):
        return super(Resource,self).__dir__() + [
            'description',
            'clasz',
            'category',
            'type',
            'factories',
        ]

    def process(self,element):
        self.category = element.name
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('name')
        self.type = '%s'%element.prop('providerType')
        self.description = '%s'%element.prop('description')
        self.clasz = '%s'%element.prop('implementationClassName')
        for f in getElements(self.ctx,'factories',element):
            factory = WebSphere.Factory(self.doc,self.ctx)
            factory.process(f)
            self.factories.append(factory)
        return

