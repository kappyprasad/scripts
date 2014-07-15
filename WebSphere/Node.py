#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Node(WebSphere.Base):
    
    @property
    def servers(self):
        return self.__servers

    @property
    def serverIndexes(self):
        return self.__serverIndexes

    def __init__(self, doc=None, ctx=None):
        super(Node,self).__init__(doc,ctx)
        self.__servers       = Types.Map('name',WebSphere.Server)
        self.__serverIndexes = Types.Map('name',WebSphere.ServerIndex)
        return

    def __dir__(self):
        return super(Node,self).__dir__() + [ 
            'servers',
            'serverIndexes',
        ]

    def process(self):
        super(Node,self).process('/topology.node:Node')
        
