
class Project(object):
    
    json = {}
    id = ''
    name = ''
    
    @property
    def doc(self):
        return '<xmi name="%s" id="%s"/>'%(self.name,self.id)
    
    def __init__(self,json):
        self.json = json
        self.id = json['@id']
        self.name = json['@name']
        return
    
    