#!/usr/bin/env python

####################################################################################
import sys,re,os,json,argparse

from Tools.xmi import *
from Tools.xpath import *
from Tools.parser import *
from Tools.finder import *

####################################################################################
parser = argparse.ArgumentParser()

fgroup = parser.add_mutually_exclusive_group()
fgroup.add_argument('-l','--link',    action='store_true', help='link local files')
fgroup.add_argument('-s','--svn',     action='store_true', help='link svn files')

parser.add_argument('-v','--verbose', action='store_true', help='show help')
parser.add_argument('-c','--cygwin',  action='store_true', help='shell is cygwin')
parser.add_argument('-f','--files',   action='store_true', help='included files')
parser.add_argument('-o','--output',  action='store',      help='output.xmi file name', default='.xmi')
parser.add_argument('dir',            action='store',      help='the directory')

args = parser.parse_args()

####################################################################################
if args.verbose:
    json.dump(vars(args),sys.stderr,indent=4)
    sys.stderr.write('\n')

####################################################################################
class RuleParser:

    fr = re.compile('^.*\.drl$')
    fg = re.compile('^.*\.gdst$')
    
    rr = re.compile('^rule [\'\"]*([^\'\"]*)[\'\"]*$')
    rq = re.compile('^query [\'\"]*([^\'\"]*)[\'\"]*$')
    ra = re.compile('^agenda-group [\'\"]*([^\'\"]*)[\'\"]*$')
    rw = re.compile('^when$')
    rt = re.compile('^then$')
    re = re.compile('^end$')
    
    #-------------------------------------------------------------------------------
    @property
    def doc(self):
        return self.xmi.doc

    #-------------------------------------------------------------------------------
    def __init__(self,xmi=XMI()):
        self.xmi = xmi
        self.classes = self.xmi.makePackage('Classes',self.xmi.modelNS)
        self.string = self.xmi.makeClass('String',self.classes)

    #-------------------------------------------------------------------------------
    def findRules(self,path):
        rules=self.xmi.makePackage('Drools',self.xmi.modelNS)
        diagram = self.xmi.makeClassDiagram('Drools',rules)
        
        for file in findFiles(path=path,fileOrDir=True,pn='^.*\.(drl|gdst)$'):
            rule = None
            if self.fr.match(file):
                rule = self.makeRuleFile(file,os.path.basename(file),parent=rules)
            if self.fg.match(file):
                rule = self.makeGdstFile(file,os.path.basename(file),parent=rules)
            if rule:
                self.xmi.addDiagramClass(rule,diagram)
        return

    #-------------------------------------------------------------------------------
    def makeGdstFile(self,file,name,parent=None,prefix=None):
        drool = self.xmi.makePackage(name,parent)
        diagram = self.xmi.makeClassDiagram(name,drool)
        
        target = self.xmi.makeClass(name,drool)
        self.xmi.makeStereotype('GDST',target)
        self.xmi.addDiagramClass(target,diagram)

        return drool

    #-------------------------------------------------------------------------------
    def makeRuleFile(self,file,name,parent=None,prefix=None):
        drool = self.xmi.makePackage(name,parent)
        diagram = self.xmi.makeClassDiagram(name,drool)
        
        rule  = None
        query = None
        group = None
        
        fp = open(file)
        for line in fp.readlines():
            line=line.rstrip('[\r\n]')
            
            if not rule and not query:
                m = self.rr.match(line)
                if m:
                    rule=m.group(1)
                    continue
                m = self.rq.match(line)
                if m:
                    query=m.group(1)
                    continue

            m = self.ra.match(line)
            if m:
                group=m.group(1)
                continue

            if self.re.match(line):
                if rule:
                    target = self.xmi.makeClass(rule,drool)
                    self.xmi.makeStereotype('Rule',target)
                    rule=None
                if query:
                    target = self.xmi.makeClass(query,drool)
                    self.xmi.makeStereotype('Query',target)
                    query=None
                if group:
                    self.xmi.makeAttribute('group',None,group,rule)
                    
                self.xmi.addDiagramClass(target,diagram)
                continue
                
        fp.close()
        return drool
    
####################################################################################
def main():
    global files
    
    dt = RuleParser()
    dt.findRules(args.dir)

    if args.output:
        sys.stderr.write('> %s\n'%args.output)
        output = open(args.output,'w')
    else:
        output= sys.stdout

    input = StringIO.StringIO('%s\n'%dt.doc)
    doParse(False,False,True,input,False,output,False,True)
    input.close()
    output.close()
    return

if __name__ == '__main__': main()
