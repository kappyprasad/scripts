
from _tools.pyson import *

import Cubetto

class Project(Cubetto.FactoryWorker):

    name = 'Project'
    keys = [
        '@id',
        '@name',
    ]
    
    def __init__(self,json,xmi,raw,verbose):
        super(Project,self).__init__(json,xmi,raw,verbose)

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
        projectCubetto = self.json['projects']['project']
        projectXMI = self.xmi.makeClass(projectCubetto['@name'], self.package)
        for key in self.keys:
            value = eval('projectCubetto%s'%dict2eval(key))
            self.xmi.makeAttribute(key, None,'%s'%value, projectXMI)
        self.xmi.makeStereotype(self.name,projectXMI)
        if not self.raw: 
            self.xmi.addDiagramClass(projectXMI,self.diagram)
        self.entities[str(projectCubetto['@id'])] = (projectXMI,projectCubetto)
        return

    def obtain(self,id=None):
        if id in self.entities.keys():
            return self.entities[id]
        return (None,None)

    def process(self):
        return
    
