#!/usr/bin/python


from Types import Object

########################################################################################################################
class MyObject(Object):

    @property 
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name
        return

    @name.deleter
    def name(self):
        del self.__name
        return

    def __dir__(self):
        return [ 'name' ]

    def __init__(self):
        self.__name = None
        self.__value = None
        return
