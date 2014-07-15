#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Cluster(WebSphere.Base):
    
    @property
    def members(self):
        return self.__members

    def __init__(self, doc=None, ctx=None):
        super(Cluster,self).__init__(doc,ctx)
        self.__members = Types.Map('name',WebSphere.Member)
        return

    def __dir__(self):
        return super(Cluster,self).__dir__() + [ 
            'members' 
        ]

    def process(self):
        super(Cluster,self).process('/topology.cluster:ServerCluster')

        for entry in getElements(self.ctx,'/topology.cluster:ServerCluster/members'):
            member = WebSphere.Member(self.doc,self.ctx,entry)
            member.process()
            self.members.append(member)
        return
         
