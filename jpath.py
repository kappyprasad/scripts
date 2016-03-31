#!/usr/bin/env python

import os,re,sys,xmltodict,json

from Tools.parser import *
from Tools.pretty import *
from Tools.jpath import *

def printXML(xml):
    myParser = MyParser(
        colour=False, 
        rformat=True,
        areturn=True,
        output=sys.stdout
    )
    myParser.parser.Parse(xml)
    del myParser
    return
    
def main():
    dir = os.path.dirname(sys.argv[0])
    fp=open('%s/_test/sample.xml'%dir)
    xml=fp.read()
    fp.close()
    
    print
    
    printXML(xml)
    
    print
              
    js = xmltodict.parse(xml)
    
    paths = [
        'prefix:root',
        'prefix:child',
    ]
    
    xpath = '/'.join(paths)
    
    print(xpath)
    jp = xpath2eval(xpath)
    print(jp)
    
    print
    
    results = jpath(js,xpath)
    
    prettyPrint(results,colour=False)

    print 
    
    xml = xmltodict.unparse(results)
    printXML(xml)
    
    return
    
if __name__ == '__main__': main()
