#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/xpath.py $
# $Id: xpath.py 11546 2014-06-04 06:05:55Z david.edson $

import sys, re, os, libxml2

def getContextFromStringWithNS(xml,argsNS=None):
    xml = re.sub(' xmlns=["\'][^"\']*["\']','',xml)

    def handler(ectx,error):
        None #sys.stderr.write('error=%s'%error)

    libxml2.registerErrorHandler(handler,'')

    doc = libxml2.parseDoc(xml)

    ctx = doc.xpathNewContext()
    nsp = {}

    nss = xml.split('xmlns:')[1:]
    pn = re.compile('^([^=]*)=["\']([^\'"]*)["\']');
    if len(nss) > 0:
        for ns in nss:
            mn = pn.match(ns)
            if mn:
                nsp[mn.group(1)] = mn.group(2)

    if argsNS:
        pn = re.compile('^xmlns:([^=]*)=(.*)$')
        for ns in argsNS:
            mn = pn.match(ns)
            if mn:
                nsp[mn.group(1)] = mn.group(2)

    for ns in nsp.keys():
        ctx.xpathRegisterNs(ns,nsp[ns])

    return (doc,ctx,nsp)

def getContextFromString(xml,argsNS=None):
    (doc,ctx,nsp) = getContextFromStringWithNS(xml,argsNS)
    return (doc,ctx)

def getContextFromFile(fn,argsNS=None):
    fp = open(fn)
    xml = ''.join(fp.readlines())
    fp.close()
    return getContextFromString(xml,argsNS)

def getElements(context,xpath,parent=None):
    if parent:
        context.setContextNode(parent)
    return context.xpathEval(xpath)

def getElement(context,xpath,parent=None):
    elements = getElements(context,xpath,parent)
    if len(elements) > 0:
        return elements[0]
    return None

def getElementText(context,xpath,parent=None):
    element = getElement(context,xpath,parent)
    if element:
        return element.content
    return None

def setElementText(context,xpath,value,parent=None):
    element = getElement(context,xpath,parent)
    if element:
        element.setContent(value)
    return

def addElement(document,name,parent=None):
    if not parent:
        parent = document.getRootElement()
    element = document.newDocNode(parent.ns(),name,None)
    parent.addChild(element)
    return element

def addElementText(document,name,value,parent=None):
    if not parent:
        parent = document.getRootElement()
    element = document.newDocNode(parent.ns(),name,value)
    parent.addChild(element)
    return element

def addElementCDATA(document,name,value,parent=None):
    element = addElement(document,name,parent=parent)
    cdata = document.newCDataBlock(value,len(value))
    element.addChild(cdata)
    return element

def delAttribute(element,attname):
    for property in element.properties:
        #sys.stderr.write('%s\n'%property)
        if property.type == 'attribute' and property.name == attname:
            property.unlinkNode()
            property.freeNode()
            break
    return
