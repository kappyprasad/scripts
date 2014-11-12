
from _tools.pyson import *
from _tools.pretty import *

import Cubetto

class ObjectType(Cubetto.FactoryWorker):
    
    name = 'ObjectType'
    
    def __init__(self,json,xmi,raw,verbose):
        super(ObjectType,self).__init__(json,xmi,raw,verbose)

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
            if 'propertyType' in objectTypeCubetto.keys():
                if type(objectTypeCubetto['propertyType']) == dict:
                    self.__processPropertyType(objectTypeCubetto['propertyType'], objectTypeXMI)
                if type(objectTypeCubetto['propertyType']) == list:
                    for propertyTypeCubetto in objectTypeCubetto['propertyType']:
                        self.__processPropertyType(propertyTypeCubetto, objectTypeXMI)
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
    
    def __processPropertyType(self, propertyTypeCubetto, objectTypeXMI):
        """
        private method to process the propertyType attribute
        """
        if self.verbose:
            sys.stderr.write('propertyTypeCubetto\n')
            prettyPrint(dict(propertyTypeCubetto),output=sys.stderr,colour=True)
        key = '@en'
        if not key in propertyTypeCubetto['name'].keys():
            key = '@key'
        self.xmi.makeAttribute(propertyTypeCubetto['name'][key], None, propertyTypeCubetto['name']['@key'], objectTypeXMI)
        return
    
