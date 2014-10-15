#!/usr/bin/python

# $Date: 2014-06-26 11:01:47 +1000 (Thu, 26 Jun 2014) $
# $Revision: 11947 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/test/ParentObject.py $
# $Id: ParentObject.py 11947 2014-06-26 01:01:47Z david.edson $

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
