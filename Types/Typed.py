#!/usr/bin/python




from Type import Type

class Typed(Type):
    
    @property
    def value(self):
        return self.__value

    def __init__(self,type):
        super(Typed,self).__init__(type)
        self.__value = None
        return
    
    def get(self):
        return self.__value

    def set(self,value):
        super(Typed,self).__validate__(value)
        self.__value = value
        return

    def delete(self):
        del self.__value

    def __dir__(self):
        return ['value']
