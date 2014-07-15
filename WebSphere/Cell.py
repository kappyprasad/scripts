#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Cell(WebSphere.Base):
    
    @property
    def clusters(self):
        return self.__clusters

    @property
    def nodes(self):
        return self.__nodes

    @property
    def applications(self):
        return self.__applications

    @property
    def virtualHosts(self):
        return self.__virtualHosts

    def __init__(self, doc=None, ctx=None):
        super(Cell,self).__init__(doc,ctx)
        self.__clusters     = Types.Map('name',WebSphere.Cluster)
        self.__nodes        = Types.Map('name',WebSphere.Node)
        self.__applications = Types.Map('name',WebSphere.Application)
        self.__virtualHosts = Types.Map('name',WebSphere.VirtualHost)
        return

    def __dir__(self):
        return super(Cell,self).__dir__() + [
            'clusters',
            'nodes',
            'applications',
            'virtualHosts' ,
        ]

    def process(self):
        super(Cell,self).process('/topology.cell:Cell')
        return

