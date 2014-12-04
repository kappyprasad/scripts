#!/usr/bin/python


from Types import Object,Typed
from MyObject import MyObject

########################################################################################################################
class ParentObject(Object):

    @property 
    def child(self):
        return self.__child.get()

    @child.setter
    def child(self,child):
        self.__child.set(child)
        return
        
    @child.deleter
    def child(self):
        self.__child.delete()
        return

    def __dir__(self):
        return [ 'child' ]

    def __init__(self):
        self.__child = Typed(MyObject)
        return
