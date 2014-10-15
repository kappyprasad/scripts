#!/usr/bin/python

# $Date: 2014-06-26 10:52:09 +1000 (Thu, 26 Jun 2014) $
# $Revision: 11946 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/test/MyObject.py $
# $Id: MyObject.py 11946 2014-06-26 00:52:09Z david.edson $

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
