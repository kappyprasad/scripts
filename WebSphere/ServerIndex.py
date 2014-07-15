#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class ServerIndex(WebSphere.Entity):
    
    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self,description):
        self.__description = description
        return

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self,type):
        self.__type = type
        return

    @property
    def applications(self):
        return self.__applications

    def __init__(self,doc=None,ctx=None):
        super(ServerIndex,self).__init__(doc,ctx)
        self.__description = None
        self.__type = None
        self.__applications = Types.List(str)
        return

    def __dir__(self):
        return super(ServerIndex,self).__dir__() + [ 
            'description',
            'type',
            'applications', 
        ]

    def process(self,element):
        self.id = '%s'%element.prop('id')
        self.name = '%s'%element.prop('serverName')
        self.type = '%s'%element.prop('serverType')
        self.display= '%s'%element.prop('serverDisplayName')
        for da in getElements(self.ctx,'deployedApplications',element):
            self.applications.append('%s'%da.content)
        return

    

