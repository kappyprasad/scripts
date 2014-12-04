#!/usr/bin/python



from Type import Type

class List(Type):

    def __init__(self):
        super(List,self).__init__()

    def __init__(self,type):
        super(List,self).__init__(type)
        self.__values = []
        return

    def __iter__(self):
        for elem in self.__values:
            yield elem

    def __len__(self):
        return len(self.__values)

    def __add__(self,value):
        self.append(value)

    def __getslice__(self,i,j):
        return self.__values[i:j]

    def __getitem__(self,key):
        if key in range(len(self.__values)):
            return self.__values[key]
        return None

    def __setitem__(self,key,value):
        super(List,self).__validate__(value)
        if key in range(len(self.__values)):
            self.__values[key] = value
        return

    def __delitem__(self,key):
        if key in range(len(self.__values)):
            del self.__values[key]
        return

    def __contains__(self,value):
        return value in self.__values

    def append(self,value):
        super(List,self).__validate__(value)
        self.__values.append(value)
        return

    def remove(self,value):
        super(List,self).__validate__(value)
        if value in self.__values:
            del self.__values[self.__values.index(value)]
        return
