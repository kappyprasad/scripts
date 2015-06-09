#!/usr/bin/env python2.7


import os,re,sys
import unittest, uuid

from Tools.test import *
from Tools.xpath import *
from Tools.pretty import *

import xpath

xml="""<?xml version="1.0" encoding="UTF-8"?>
<prefix:root attr="bob &lt; &gt; &amp; &quot; &apos; char" xmlns:prefix="http://www.mucken.com.au/Sample" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.mucken.com.au/Sample Sample.xsd">
    <prefix:child>stuff &lt;inside&gt; &quot; &apos;</prefix:child>
    <prefix:child>hello</prefix:child>
    <prefix:child there="normal"/>
    <prefix:daughter><![CDATA[<hello & ' " &amp; there/>]]></prefix:daughter>
</prefix:root>
"""

class Xpath_1_ToolsTest(unittest.TestCase):
    """xpath tools module test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_XpathSearchFile(self):
        """search xpath nodes in file(s) assuming wrapped results"""
        fn = '%s/%s.xml'%(os.environ['TEMP'],uuid.uuid4())
        print fn
        fp = open(fn,'w')
        fp.write(xml)
        fp.close()

        (doc,ctx) = getContextFromFile(fn)
        assert ctx
        assert doc

        node = getElement(ctx,'/')
        assert node
        print 'type=%s'%node.type
        assert node.type == 'document_xml'

        element = node.getRootElement()
        assert element
        print 'name=%s'%element.name
        assert element.name == 'root'

        ns = element.ns()
        print 'ns=%s'%ns
        
        os.unlink(fn)
        return

    def test_02_XpathSearchDocument(self):
        """search xpath document nodes from sys.stdin"""
        (doc,ctx) = getContextFromString(xml)
        assert ctx
        assert doc

        node = getElement(ctx,'/')
        assert node
        print 'type=%s'%node.type
        assert node.type == 'document_xml'

        element = node.getRootElement()
        assert element
        print 'name=%s'%element.name
        assert element.name == 'root'

        ns = element.ns()
        print 'ns=%s'%ns
        return

    def test_03_XpathSearchElement(self):
        """search for xpath element node """
        argsNS = ['xmlns:prefix=http://www.mucken.com.au/Sample']
        (doc,ctx) = getContextFromString(xml,argsNS)
        assert ctx
        assert doc

        node = getElement(ctx,'//prefix:daughter')
        assert node
        print 'type=%s'%node.type
        assert node.type == 'element'

        element = node
        assert element
        print 'name=%s'%element.name
        assert element.name == 'daughter'

        ns = element.ns()
        print 'ns=%s'%ns
        return
    
    def test_04_XpathSearchText(self):
        """search for xpath text and display text part"""
        argsNS = ['xmlns:prefix=http://www.mucken.com.au/Sample']
        (doc,ctx) = getContextFromString(xml,argsNS)
        assert ctx
        assert doc

        node = getElementText(ctx,'//prefix:child[2]')
        assert node
        print 'type=%s'%type(node)
        assert '%s'%type(node) == '<type \'str\'>'

        print 'name=%s'%node
        assert node == 'hello'
        return
    
    def test_05_XpathSearchAttribute(self):
        """search for xpath attribute and display text part"""
        argsNS = ['xmlns:prefix=http://www.mucken.com.au/Sample']
        (doc,ctx) = getContextFromString(xml,argsNS)
        assert ctx
        assert doc

        node = getElementText(ctx,'//prefix:child[3]/@there')
        assert node
        print 'type=%s'%type(node)
        assert '%s'%type(node) == '<type \'str\'>'

        print 'name=%s'%node
        assert node == 'normal'
        return


if __name__ == '__main__':
    unittest.main()
