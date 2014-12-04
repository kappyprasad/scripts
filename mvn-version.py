#!/usr/bin/python




import sys,os,re
import argparse

from _tools.colours import *
from _tools.xpath import *
from _tools.parser import *
from _tools.eddo import *
from _tools.finder import *
from _tools.pretty import *

parser = argparse.ArgumentParser()

parser.add_argument('-v','--verbose',    action='store_true', help='verbose mode')
parser.add_argument('-d','--display',    action='store_true', help='display only')
parser.add_argument('-m','--modules',    action='store_true', help='show module heirarchy')
parser.add_argument('-t','--tag',        action='store',      help='tag version name')
parser.add_argument('-g','--groupId',    action='store',      help='groupId',    metavar='groupId',            nargs='*')
parser.add_argument('-a','--artifactId', action='store',      help='artifactId', metavar='groupId.artifactId', nargs='*')
parser.add_argument('dir',               action='store',      help='directories to process',                   nargs='*')

args = parser.parse_args()

if args.verbose:
    print 'args='
    printer = PrettyPrinter(colour=True)
    printer.prettify(var(args))
    del printer

(prefix,namespace) = ('mvn','http://maven.apache.org/POM/4.0.0')

target=re.compile('.*/target/.*')

horizon=buildHorizon()


logged='{0}{1:<30.30} {2:<30.30}' + colours['Off'] + ' {3:<30.30} {4:<30.30}'
changed=logged.replace('{3','%s{3'%colours['Red']).replace('{4','%s{4'%colours['Green'])+colours['Off']

thisversion = colours['Teal'] + ' |--'
themodules  = colours['Teal'] + '  \_'
thatversion =                   '  \_'

groupIds = { 
    # groupId : {
    #      artifactId  : {
    #          'version' : '',
    #          'modules' : [
    #              artifactId
    #          ]
    #     }
    # } 
}

def get(ctx,node):
    groupId =    getElementText(ctx,'groupId',node)
    artifactId = getElementText(ctx,'artifactId',node)
    version =    getElementText(ctx,'version',node)
    return (groupId,artifactId,version)

def set(ctx,node,version):
    if node and version:
        setElementText(ctx,'version',version,node)
    return

def save(pom,doc):
    bak='%s.bak'%pom
    try:
        os.remove(bak)
    except:
        None
    os.rename(pom,bak)

    fp = open(pom,'w')

    p = MyParser(colour=False,output=fp,rformat=True)
    try:
        p.parser.Parse('%s'%doc)
    except:
        fp.write('%s'%doc)
    del p

    fp.close()

    return

def load(pom):
    (doc,ctx) = getContextFromFile(pom)

    project = getElement(ctx,'/project')
    (groupId,artifactId,version) = get(ctx,project)

    if not groupId in groupIds.keys():
        groupIds[groupId] = {}

    this = {}
    groupIds[groupId][artifactId] = this

    this['version' ] = version

    if getElementText(ctx,'packaging',project) == 'pom':
        this['modules' ] = {}
        for module in getElements(ctx,'modules/module',project):
            this['modules'][module.content] = {}

    parent = getElement(ctx,'parent',project)
    if parent:
        this['parent'] = {
            'groupId' : getElementText(ctx,'groupId',parent),
            'artifactId' : getElementText(ctx,'artifactId',parent)
        }
    return

def treeify():
    removals = {
        # groupId : [
        #      artifactId
        # ]
    }
    
    for groupId in groupIds.keys():
        for artifactId in groupIds[groupId].keys():
            child = groupIds[groupId][artifactId]
            if 'parent' in child.keys():
                prettyPrint(child)
                gParent = child['parent']['groupId']
                aParent = child['parent']['artifactId']
                if gParent in groupIds.keys():
                    if aParent in groupIds[gParent].keys():
                        parent = groupIds[gParent][aParent]
                        if not groupId in removals.keys():
                            removals[groupId] = []
                            removals[groupId].append(artifactId)

    for groupId in removals.keys():
        for artifactId in removals[groupId]:
            del groupIds[groupId][artifactId]
        if len(groupIds[groupId]) == 0:
            del groupIds[groupId]

    return

def update(pom):
    (doc,ctx) = getContextFromFile(pom)

    project = getElement(ctx,'/project')
    (groupId,artifactId,version) = get(ctx,project)
    
    if args.tag \
    and (groupId in groupIds.keys() and artifactId in groupIds[groupId].keys()) \
    or (args.groupId and groupId in args.groupId) \
    or (args.artifactId and artifactId in args.artifactId) \
    :
        set(ctx,project,args.tag)
        sys.stderr.write('%s\n'%changed.format(thisversion,groupId,artifactId,version,args.tag))
    else:
        sys.stderr.write('%s\n'%logged.format(thisversion,groupId,artifactId,version,''))

    for module in getElements(ctx,'/project/modules/module'):
        sys.stderr.write('%s\n'%logged.format(themodules,'_'*30,module.content,'',''))
        
    for dependency in getElements(ctx,'//dependency'):
        (groupId,artifactId,version) = get(ctx,dependency)

        if args.tag \
        and (groupId in groupIds.keys() and artifactId in groupIds[groupId].keys()) \
        or (args.groupId and groupId in args.groupId) \
        or (args.artifactId and artifactId in args.artifactId) \
        :
            set(ctx,dependency,args.tag)
            sys.stderr.write('%s\n'%changed.format(thatversion,groupId,artifactId,version,args.tag))
        else:
            sys.stderr.write('%s\n'%logged.format(thatversion,groupId,artifactId,version,''))
        
    del ctx
    
    if args.tag and not args.display:
        save(pom,doc)

    del doc

    return

def main():
    dirs = ['.']
    if args.dir:
        dirs = args.dir

    for dir in dirs:
        for pom in findFiles(dir,True,'^pom.xml$'):
            if not target.match(pom):
                load(pom)


    if args.modules:
        treeify()
        prettyPrint(groupIds)
        return

    for dir in dirs:
        for pom in findFiles(dir,True,'^pom.xml$'):
            sys.stderr.write('%s\n'%horizon)
            if not target.match(pom):
                sys.stderr.write('%s%s%s\n'%(colours['Orange'],pom,colours['Off']))
                update(pom)
    return

if __name__ == '__main__': main()
