#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Server(WebSphere.Base):
    
    @property
    def applications(self):
        return self.__applications

    def __init__(self, doc=None, ctx=None):
        super(Server,self).__init__(doc,ctx)
        self.__applications = Types.Map('name',WebSphere.Application)
        return

    def __dir__(self):
        return super(Server,self).__dir__() + [ 
            'applications' 
        ]

    def process(self):
        super(Server,self).process('/process:Server')
        return

