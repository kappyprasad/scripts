#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from _tools.xpath import *

import Types
import WebSphere

class Application(WebSphere.Base):

    @property
    def modules(self):
        return self.__modules

    def __init__(self,doc=None,ctx=None):
        super(Application,self).__init__(doc,ctx)
        self.__modules = Types.Map('name',WebSphere.Module)
        return

    def __dir__(self):
        return super(Application,self).__dir__() + [ 
            'modules', 
        ]

    def process(self):
        element = getElement(self.ctx,'/application') 
        self.id = '%s'%element.prop('id')
        self.name = getElementText(self.ctx,'display-name',element)
        for m in getElements(self.ctx,'module',element):
            module = WebSphere.Module(self.doc,self.ctx)
            module.process(m)
            self.modules.append(module)
        return

