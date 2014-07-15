#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




from _tools.xpath import *

import Types
import WebSphere

class Package(WebSphere.Entity):
    

    def __init__(self, doc=None,ctx=None):
        super(Package,self).__init__(doc,ctx)
        return

    def export(self,xmi,parent):
        package = xmi.makePackage(self.name,parent)
        xmi.makeStereotype(self.__class__.__name__,package)
        diagram = xmi.makeClassDiagram(self.name,package)

        for key in dir(self):
            obj = getattr(self,key)

            if isinstance(obj,Types.Map) or isinstance(obj,Types.List):

                subPackage = xmi.makePackage(key,package)
                xmi.addDiagramClass(subPackage,diagram)
                subDiagram = xmi.makeClassDiagram(key,subPackage)

                for item in obj:
                    if isinstance(item,WebSphere.Entity):
                        clasz = item.export(xmi,subPackage)
                        if clasz != None:
                            xmi.addDiagramClass(clasz,subDiagram)
                    elif isinstance(item,WebSphere.Package):
                        pkg = item.export(xmi,subPackage)
                        if pkg != None:
                            xmi.addDiagramClass(pkg,subDiagram)

            if isinstance(obj,WebSphere.Entity):
                clasz = obj.export(xmi,package)
                if clasz != None:
                    xmi.addDiagramClass(clasz,diagram)

        return package
