#!/usr/bin/python

# $Date$
# $Revision$
# $Author$
# $HeadURL$
# $Id$




# http://mikekneller.com/kb/python/libxml2python/part1

import sys,os,argparse,StringIO

from _tools.xpath import *

horizon = ''
if 'COLUMNS' in os.environ:
    horizon = '-' * int(os.environ['COLUMNS'])
else:
    horizon = '-' * 80

def comma(count,output):
    if count > 0:
        output.write(',')
    count+=1
    return count

def text2json(content,output,indent):
    output.write('\n%s"!CDATA" : "%s"'%(indent,content))
    return

def property2json(property,output,indent):
    output.write('\n%s"@%s" : "%s"'%(indent,property.name, property.content))
    return

def node2json(node,output,indent):
    count=0
    if node.properties:
        for property in node.properties:
            if property.type == 'attribute':
                count = comma(count,output)
                property2json(property,output,indent='%s    '%indent)
    children=False
    if node.children:
        elements = {}
        for child in node.children:
            if child.type == 'element':
                children=True
                if child.name not in elements.keys():
                    elements[child.name] = []
                elements[child.name].append(child)
        for key in elements.keys():
            if len(elements[key]) > 1:
                count = comma(count,output)
                array2json(key,elements[key],output,indent='%s    '%indent)
            else:
                count = comma(count,output)
                element2json(elements[key][0],output,indent='%s    '%indent)
                del elements[key][0]
    if not children and node.content:
        count = comma(count,output)
        text2json(node.content,output,indent='%s    '%indent)
    return

def array2json(name,elements,output,indent):
    output.write('\n%s"%s" : ['%(indent,name))
    count = 0
    for element in elements:
        count = comma(count,output)
        output.write('\n%s    {'%indent)
        node2json(element,output,indent='%s    '%indent)
        output.write('\n%s    }'%indent)
    output.write('\n%s]'%indent)

def element2json(element,output,indent):
    output.write('\n%s"%s" : { '%(indent,element.name))
    node2json(element,output,indent)
    output.write('\n%s}'%indent)
    return

def doc2json(doc,ctx,output):
    output.write('{')
    element2json(doc.getRootElement(),output,indent='    ')
    output.write('\n}\n')
    return

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-?',              action='help',       help='show this help')
    parser.add_argument('-v','--verbose',  action='store_true', help='show detailed output')
    parser.add_argument('-c','--colour',   action='store_true', help='show output in colour')
    parser.add_argument('-b','--bar',      action='store_true', help='put horizontal bar inbetween')
    parser.add_argument('-t','--title',    action='store_true', help='display file name as title')
    parser.add_argument('-o','--output',   action='store',      help='output to xml file')
    parser.add_argument('-H','--html',     action='store',      help='output in HTML file')
    parser.add_argument('file',            action='store',      help='files to format', nargs='*')

    args = parser.parse_args()

    colour = args.colour

    output = sys.stdout

    foutput = args.output
    if foutput:
        colour = False
        print foutput
        output = open(foutput,'w')

    houtput = args.html
    if houtput:
        html = True
        print houtput
        output = open(houtput,'w')
    else:
        html = False
    
    title = args.title

    if args.file:
        for arg in args.file:
            f = arg

            if args.bar:
                print horizon
            if title:
                print f
            (doc,ctx) = getContextFromFile(f)
            doc2json(doc,ctx,output)
    else:
        fp = StringIO.StringIO('\n'.join(sys.stdin.readlines()))
        (doc,ctx) = getContextFromString(fp.getvalue())
        doc2json(doc,ctx,output)
        fp.close()
        
    if foutput:
        output.close()

    return
    
if __name__ == '__main__': main()

