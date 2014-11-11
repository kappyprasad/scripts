
from _tools.pyson import *

import Cubetto

class ObjectType(Cubetto.FactoryWorker):
    
    name = 'ObjectType'
    keys = [
        '@id',
        'name.@en'
    ]
    
    def __init__(self,json,xmi,raw):
        super(ObjectType,self).__init__(json,xmi,raw)

        self.package = xmi.makePackage(self.name,self.xmi.modelNS)
        if not self.raw: 
            self.diagram = xmi.makeClassDiagram(self.name, self.package)
            print 'ClassDiagram(%s) : %s'%(
                self.name,
                self.diagram.parent.prop('xmi.id')
            )
        
        return

    def __del__(self):
        return

    def ingest(self):
        for objectTypeCubetto in self.json['projects']['project']['modelType']['objectType']:
            objectTypeXMI = self.xmi.makeClass(objectTypeCubetto['name']['@en'], self.package)
            for key in self.keys:
                value = eval('objectTypeCubetto%s'%dict2eval(key))
                self.xmi.makeAttribute(key, None,'%s'%value, objectTypeXMI)
            self.xmi.makeStereotype(self.name,objectTypeXMI)
            if not self.raw: 
                self.xmi.addDiagramClass(objectTypeXMI,self.diagram)
            self.entities[str(objectTypeCubetto['@id'])] = (objectTypeXMI,objectTypeCubetto)
        return

    def obtain(self,id=None):
        if id in self.entities.keys():
            return self.entities[id]
        return (None,None)

    def process(self):
        return
    
