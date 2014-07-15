#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$


class Type(object):

    def __init__(self):
        raise TypeError('%s.__init__(?), must define a type'%self.__class__)

    def __init__(self,type):
        self.__type = type
        return

    def __validate__(self,value):
        if not isinstance(value,self.__type):
            raise TypeError('%s must be of type %s'%(value,self.__type))
        return

    @property
    def type(self):
        return '%s'%self.__type.__name__

    
    
