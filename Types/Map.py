#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


from Type import Type

class Map(Type):

    def __init__(self):
        super(Map,self).__init__()

    def __init__(self,key,type):
        super(Map,self).__init__(type)
        self.__key = key
        self.__values = {}
        return

    def __key__(self,value):
        if not self.__key in dir(value):
            raise TypeError('%s has no %s attribute'%(value,self.__key))
        return getattr(value,self.__key)

    def __iter__(self):
        for key in self.__values.keys():
            yield self.__values[key]

    def __len__(self):
        return len(self.__values)

    def __add__(self,value):
        self.append(value)

    def __getslice__(self,i,j):
        return self.__values[i:j]

    def __getitem__(self,key):
        if key in self.__values.keys():
            return self.__values[key]
        return None

    def __setitem__(self,key,value):
        super(Map,self).__validate__(value)
        self.__values[key] = value
        return

    def __delitem__(self,key):
        if key in self.__values.keys():
            del self.__values[key]
        return

    def __contains__(self,value):
        key = getattr(value,self.__key)
        return key in self.__values.keys()

    @property
    def key(self):
        return self.__key

    def keys(self):
        return self.__values.keys()

    def append(self,value):
        super(Map,self).__validate__(value)
        key = self.__key__(value)
        self.__values[key] = value
        return

    def remove(self,value):
        key = self.__key__(value)
        if key in self.__values.keys():
            del self.__values[key]
        return

