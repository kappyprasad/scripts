
import json

from _tools.pyson import *
from _tools.pretty import *

import Cubetto

class PropertyType(Cubetto.FactoryWorker):
    
    name = 'PropertyType'
    languages = ['@en','@en-GB','@dn']

    def __init__(self,json,xmi,raw,verbose):
        super(PropertyType,self).__init__(json,xmi,raw,verbose)

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
            if not 'propertyType' in objectTypeCubetto.keys():
                continue
            if not type(objectTypeCubetto['propertyType']) == list:
                l = []
                l.append(objectTypeCubetto['propertyType'])
            else:
                l = objectTypeCubetto['propertyType']
            for propertyTypeCubetto in l:
                object=None
                for key in self.languages:
                    if key in propertyTypeCubetto['name'].keys():
                        object =  propertyTypeCubetto['name'][key]
                        break
                propertyTypeXMI = self.xmi.makeClass(object, self.package)
                self.xmi.makeStereotype(self.name,propertyTypeXMI)
                if not self.raw: 
                    self.xmi.addDiagramClass(propertyTypeXMI,self.diagram)
                self.entities[str(propertyTypeCubetto['@id'])] = (propertyTypeXMI,propertyTypeCubetto)
                for attr in ['@max','@min','@index']:
                    self.xmi.makeAttribute(propertyTypeCubetto[attr], None, None, propertyTypeXMI)

        return

    def obtain(self,id=None):
        if id in self.entities.keys():
            return self.entities[id]
        return (None,None)

    def process(self):
        for key in self.entities.keys():
            entity = self.entities[key]
            
        return
    
