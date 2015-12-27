#!/usr/bin/env python





host='dhcp-048.ipdbdemo.cba'
port='19086'

from xml.dom.minidom import parse, Document, Node
import sys, re, os, urllib, urllib2, StringIO
import argparse

from Tools.colours import *
from Tools.eddo import *
from Tools.xpath import *
from Tools.parser import *
from Tools.cdata import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',    action='store_true',  help='versbose mode')
parser.add_argument('-u','--ignorecase', action='store_true',  help='case insensitive')
parser.add_argument('-c','--colour',     action='store_true',  help='output in colour')
parser.add_argument('-g','--guid',       action='store_true',  help='show guids')
parser.add_argument('-s','--system',     action='store_true',  help='show system toolkit matches')
parser.add_argument('-x','--xpath',      action='store',       help='xpath filter on element')
parser.add_argument('-H','--html',       action='store',       help='output to html file')
parser.add_argument('search',            action='store',       help='search string regex compatible')

args = parser.parse_args()

tab='\t'

cp = re.compile('^.*\s(\S+\.class)$')
jar = re.compile('^.*\.jar$')
fn = re.compile('.*(function).*')

colour=False

def findFiles(path='.', fileOrDir=True, pn='^.*$'):
    files = []
    p = re.compile(pn)
    for f in os.listdir('%s'%path):
        fp = '%s/%s'%(path,f)
        if os.path.isfile(fp):
            # is a file
            if p.match(f) and fileOrDir:
                # matches and are looking for files
                files.append(fp)
        elif os.path.isdir(fp):
            #is a dir
            if p.match(f) and not fileOrDir:
                files.append(fp)
            files += findFiles(fp, fileOrDir, pn)
    return files

def processFolder(bd, td, search, fh=sys.stdout):
    if td:
        color = colours['Green']
        d=td
    else:
        color = colours['Purple'] 
        d=bd
        
    (project, toolkits, objects, files, assets) = getPackage(d)
    #if not project:
    #    return

    fh.write('%s%s%s%s (%s)%s\n'%(html,color,project['name'],colours['Off'],project['sname'],lmth))
    fh.flush()
    
    types = {}
    
    for key in objects.keys():
        f = '%s/objects/%s.xml'%(d,key)
        fp = open(f)
        doc = parse(f)
        types = getTypes(doc, types, search)
        fp.close()
        
    printTypes(types,fh=fh)
    processClasses(d, td, search, files, assets,fh=fh)
    processFiles(d, td, search, files, assets,fh=fh)

    fh.write('\n')
    fh.flush()
        
    for key in toolkits.keys():
        (sid,sname) = toolkits[key]
        
        p = '%s/toolkits/%s.zip.exploded'%(bd,sid)
        processFolder(bd, p, search,fh=fh)

    return

def escapeLine(line):
    line = line.replace('&','&amp;')
    line = line.replace('<','&lt;')
    line = line.replace('>','&gt;')
    return line
    
def processClasses(d, td, search, files, assets, fh=sys.stdout):
    if args.xpath:
        return
    classes = {}

    if not os.path.isdir('%s/files'%d):
        return

    for i in files.keys():
        name = assets[i]
        path = files[i]
        f = '%s/files/%s/%s.jar.log'%(d,i,path)
        if not jar.match(name):
            continue
        if not os.path.isfile('%s'%f):
             continue

        founds = []
        fp = open(f,'r')
        for line in fp.readlines():
            cm = cp.match(line)
            if cm:
                cl = cm.group(1)
                if search:
                    sm = search.match(cl)
                    if sm:
                        if html:
                            cl = escapeLine(cl)
                        found = sm.group(1)
                        founds.append(cl.replace(found, colours['Red'] + found + colours['Off']))
                else:
                    founds.append(cl)
        if len(founds) > 0:
            classes[name] = founds

    if len(classes) > 0:
        fh.write('%s%s%sclasses ...%s%s\n'%(html,tab*1,colours['Teal'],colours['Off'],lmth))
        fh.flush()
        for clasz in classes.keys():
            founds = classes[clasz]
            if len(founds) > 0:
                fh.write('%s%s%s%s%s%s\n'%(html,tab*2,colours['Orange'],clasz,colours['Off'],lmth))
                fh.flush()
                for found in founds:
                    fh.write('%s%s%s%s\n'%(html,tab*3,found,lmth))
        
    return

def processFiles(d, td, search, files, assets, fh=sys.stdout):
    ascii = {}
    if not os.path.isdir('%s/files'%d):
        return

    for i in files.keys():
        name = assets[i]
        path = files[i]
        f = '%s/files/%s/%s.txt'%(d,i,path)
        if jar.match(name):
            continue
        if not os.path.isfile('%s'%f):
             continue

        founds = []
        fp = open(f,'r')
        for line in fp.readlines():
            if search:
                sm = search.match(line)
                if sm:
                    if html:
                        line = escapeLine(line)
                    found = sm.group(1)
                    founds.append(line.replace(found, colours['Red'] + found + colours['Off']))
            else:
                fm = fn.match(line)
                if fm:
                    if html:
                        line = escapeLine(line)
                    found = fm.group(1)
                    founds.append(line.replace(found, colours['Red'] + found + colours['Off']))
                    
        if len(founds) > 0:
            ascii[name] = founds

    if len(ascii) > 0:
        fh.write('%s%s%sfiles ...%s%s\n'%(html,tab*1,colours['Teal'],colours['Off'],lmth))
        fh.flush()
        for key in ascii.keys():
            founds = ascii[key]
            if len(founds) > 0:
                fh.write('%s%s%s%s%s%s\n'%(html,tab*2,colours['Orange'],key,colours['Off'],lmth))
                fh.flush()
                for found in founds:
                    fh.write('%s%s%s%s\n'%(html,tab*3,found,lmth))
        
    return

def getPackage(path):
    global processedToolkits

    fp = '%s/META-INF/package.xml'%path
    #if not os.access(fp,os.F_OK): 
    #    return (None, None, None)
    
    project = {}
    toolkits = {}
    objects = {}
    assets = {}
    files = {}

    (package,context) = getContextFromFile(fp)

    project['name'] = getElementText(context,'/p:package/target/project/@name')
    project['sid']  = getElementText(context,'/p:package/target/snapshot/@id')
    project['sname'] = getElementText(context,'/p:package/target/snapshot/@name')
    
    for dependency in getElements(context,'/p:package/dependencies/dependency'):
        isSystem = getElementText(context,'project/@isSystem',dependency)
        if isSystem == 'false' or args.system:
            pname = getElementText(context,'project/@name',dependency)
            vname = getElementText(context,'snapshot/@id',dependency)
            sname = getElementText(context,'snapshot/@name',dependency)
            if pname not in processedToolkits:
                toolkits[pname] = (vname,sname)
                processedToolkits.append(pname)

    for objekt in getElements(context,'/p:package/objects/object'):
        if objekt.prop('type') == 'managedAsset':
            assets[objekt.prop('id')] = objekt.prop('name')
        else:
            objects[objekt.prop('id')] = objekt.prop('name')
    
    for fe in getElements(context,'p:package/files/file'):
        files[fe.prop('id')] = fe.prop('path')

    return (project, toolkits, objects, files, assets)

def getSchema(variable, version):
    url = 'http://%s:%s/webapi/ViewSchema.jsp?type=%s&version=%s'%(
        host, port, variable, version
    )
    response = urllib2.urlopen(url)
    xsd = response.read()
    response.close()
    return xsd

def getTypes(doc, types, search=None):
    root = doc.documentElement
    for node in root.childNodes:
        if node.nodeType == Node.ELEMENT_NODE:
            tipe = node.nodeName
            if tipe not in types.keys():
                types[tipe] = {}
            name = node.getAttribute('name')
            #items = getItems(node,search)
            items = getFounds(node,search)
            if len(items) > 0 or args.verbose:
                types[tipe][name] = items
    return types

def getItems(node, search=None):
    items = {}
    for item in node.getElementsByTagName('item'):
        name = item.getElementsByTagName('name')[0].firstChild.data
        comp = item.getElementsByTagName('tWComponentName')[0].firstChild.data
        founds = getFounds(node, search)
        if len(founds) > 0 or args.verbose:
            items['%s:%s'%(comp,name)] = founds
    return items

def getFounds(node, search=None):
    founds = []
    if args.xpath and search:
        (doc,ctx)=getContextFromString(node.toxml())
        res = ctx.xpathEval(search)
        for r in res:
            output = StringIO.StringIO()
            myParser = MyParser(colour=colour,output=output,html=html)
            myParser.parser.Parse('%s'%r)
            del myParser
            ov = output.getvalue()
            if html:
                ov = '<p>%s</p>'%ov
            output.close()
            founds.append('\n%s'%ov)
    elif search:
        for line in node.toxml().split('\n'):
            match = search.match(line)
            if match:
                if html:
                    line = escapeLine(line)
                found = match.group(1)
                founds.append(line.lstrip().replace(found, colours['Red'] + found + colours['Off']))
    return founds

def printTypes(types, fh=sys.stdout):
    count = 0
    for tipe in types.keys():
        count += len(types[tipe])

    if count == 0:
        return
    
    for tipe in types.keys():
        tname = tipe.replace('process','service')
        fh.write('%s%s%s%s ...%s%s\n'%(html,tab*1,colours['Teal'],tname,colours['Off'],lmth))
        fh.flush()
            
        names = types[tipe]
        for name in names.keys():
            fh.write ('%s%s%s%-50s%s%s\n'%(html,tab*2,colours['Orange'],name,colours['Off'],lmth))
            fh.flush()
            
            founds = names[name]
            for found in founds:
                fh.write('%s%s%s%s\n'%(html,tab*3,found,lmth))
                fh.flush()

    return

def main():
    global lmth,tab,html,colour,colours,processedToolkits

    horizon = buildHorizon()

    colours = getColours()
    colour = args.colour
    if not colour:
        for key in colours.keys():
            colours[key] = ''
        
    if args.html:
        colour = False
        html = '<p>'
        lmth = '</p>'
        horizon = '<hr/>'
        tab='&nbsp'*8
        colours = getColours(html=True)
    else:
        html = ''
        lmth = ''
        
    if args.search:
        if args.xpath:
            search = args.search
        else:
            if args.ignorecase:
                search = re.compile('.*(%s).*'%args.search,re.IGNORECASE)
            else:
                search = re.compile('.*(%s).*'%args.search)
    else:
        search = None

    if args.html:
        fh = open(args.html, 'w')
        fh.write('<html><body>\n')
    else:
        fh = sys.stdout

    for d in findFiles('.',False,'^.*\.twx\.exploded$'):
        #sys.stderr.write('%s\n'%d)
        fh.write('%s\n'%horizon)
        fh.flush()
        processedToolkits = []
        processFolder(d,None,search,fh=fh)    

    if args.html:
        fh.write('</body></html>\n')
        fh.close()

    return

if __name__ == '__main__' : main()

