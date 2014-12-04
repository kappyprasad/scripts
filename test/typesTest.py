#!/usr/bin/python


import os,re,sys
import unittest, uuid

from _tools.test import *
from _tools.pretty import *

from Types import Object,Typed,Type,List,Map

from MyObject import MyObject
from ParentObject import ParentObject
from OtherObject import OtherObject

########################################################################################################################
class Types_Test(unittest.TestCase):
    """types module test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_Type(self):
        """type test class."""

        parent = ParentObject()
        
        with self.assertRaises(TypeError):
            parent.child = OtherObject()

        string = 'helloyou'

        parent.child = MyObject()
        parent.child.name = string
        self.assertIsNotNone(parent.child)
        self.assertIsInstance(parent.child,MyObject)
        self.assertEquals(string,parent.child.name)
        prettyPrint(parent)

        del parent.child
        
        with self.assertRaises(AttributeError):
            print parent.child

        return

    def test_02_List(self):
        """list test class."""

        list = None
        with self.assertRaises(TypeError):
            list = List()
            sys.stderr.write('should not see me\n')

        list = List(MyObject)
        self.assertIsNotNone(list)
        self.assertIsInstance(list,List)

        obj1 = MyObject()
        obj1.name = 'hello1'

        obj2 = MyObject()
        obj2.name = 'hello2'

        list.append(obj1)
        self.assertIn(obj1,list)

        list.append(obj2)
        self.assertIn(obj2,list)

        prettyPrint(list)

        list.remove(obj1)
        self.assertNotIn(obj1,list)

        return

    def test_03_Map(self):
        """map test class."""
        
        map = None
        with self.assertRaises(TypeError):
            map = Map()
            sys.stderr.write('should not see me\n')

        map = Map('name',MyObject)
        self.assertIsNotNone(map)
        self.assertIsInstance(map,Map)

        obj1 = MyObject()
        obj1.name = 'hello1'

        obj2 = MyObject()
        obj2.name = 'hello2'

        map.append(obj1)
        self.assertIn(obj1,map)

        map.append(obj2)
        self.assertIn(obj2,map)

        prettyPrint(map)

        map.remove(obj1)
        self.assertNotIn(obj1,map)
        
        return

    def test_04_ListString(self):
        """list strings test class."""

        list = None
        with self.assertRaises(TypeError):
            list = List()
            sys.stderr.write('should not see me\n')

        list = List(str)
        self.assertIsNotNone(list)
        self.assertIsInstance(list,List)

        list.append('one')
        self.assertIn('one',list)

        list.append('two')
        self.assertIn('two',list)

        prettyPrint(list)

        list.remove('one')
        self.assertNotIn('one',list)

        return

if __name__ == '__main__':
    unittest.main()
