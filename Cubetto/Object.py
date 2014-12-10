
from _tools.pyson import *
from _tools.pretty import *

import Cubetto

class Object(Cubetto.FactoryWorker):
    
    name = 'Object'
    languages = ['@en','@en-GB','@dn']

    def __init__(self,json,xmi,raw,verbose):
        super(Object,self).__init__(json,xmi,raw,verbose)

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
        for objectTypeCubetto in self.json['projects']['project']['modelType']['model']['object']:
            for key in self.languages:
                if key in objectTypeCubetto['name'].keys():
                    object =  objectTypeCubetto['name'][key]
                    break
            objectTypeXMI = self.xmi.makeClass(object, self.package)
            if 'e3Property' in objectTypeCubetto.keys():
                if type(objectTypeCubetto['e3Property']) == dict:
                    self.__processPropertyType(objectTypeCubetto['e3Property'], objectTypeXMI)
                if type(objectTypeCubetto['e3Property']) == list:
                    for propertyTypeCubetto in objectTypeCubetto['e3Property']:
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
        for key in self.entities.keys():
            entity = self.entities[key]
            
        return
    
    def __processPropertyType(self, propertyTypeCubetto, objectTypeXMI):
        """
        private method to process the propertyType attribute
        """
        if self.verbose:
            sys.stderr.write('propertyTypeCubetto\n')
            prettyPrint(dict(propertyTypeCubetto),output=sys.stderr,colour=True)
        property = None
        #propertyType = self.factory.obtain(type='PropertyType',id=propertyTypeCubetto['@propertyType'])
        #if '@objectValue' in propertyTypeCubetto.keys():
        #    property = self.factory.obtain(type='Object',id=propertyTypeCubetto['@objectValue'])
        #if '@propertyValue' in propertyTypeCubetto.keys():
        #    property = self.factory.obtain(type='PresentationProperty',id=propertyTypeCubetto['@propertyValue'])
        if property:
            self.xmi.makeAttribute(property['name'], None, None, objectTypeXMI)
        return
    
