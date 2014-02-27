#!/usr/bin/python

import sys, re, os, libxml2

def getContextFromFile(fn):
    fp = open(fn)
    xml = ''.join(fp.readlines())
    fp.close()
    return getContextFromString(xml)

def getContextFromString(xml):
    xml = re.sub(' xmlns=["\'][^"\']*["\']','',xml)

    doc = libxml2.parseDoc(xml)
    ctx = doc.xpathNewContext()
    pn = re.compile('^([^=]*)=["\']([^\'"]*)["\']');
    nss = xml.split('xmlns:')[1:]
    if len(nss) > 0:
        for ns in nss:
            mn = pn.match(ns)
            if mn:
                (n,h) = (mn.group(1), mn.group(2))
                #print (n,h)
                ctx.xpathRegisterNs(n,h)
    return (doc,ctx)

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
