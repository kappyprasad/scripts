#!/usr/bin/env python2.7

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

    rr = re.compile('^rule [\'\"]*([^\'\"]*)[\'\"]*$')
    ra = re.compile('^agenda-group [\'\"]*([^\'\"]*)[\'\"]*$')
    rw = re.compile('^when$')
    rt = re.compile('^then$')
    re = re.compile('^end$')
    
    @property
    def doc(self):
        return self.xmi.doc

    def __init__(self,xmi=XMI()):
        self.xmi = xmi
        self.classes = self.xmi.makePackage('Classes',self.xmi.modelNS)
        self.string = self.xmi.makeClass('String',self.classes)

    def findRules(self,path):
        rules=self.xmi.makePackage('Drools',self.xmi.modelNS)
        for file in findFiles(path=path,fileOrDir=True,pn='^.*.drl$'):
            self.makeRuleFile(file,os.path.basename(file),parent=rules)
        return
    
    def makeRuleFile(self,file,name,parent=None,prefix=None):
        drool = self.xmi.makePackage(name,parent)
        diagram = self.xmi.makeClassDiagram(name,drool)
        
        name = None
        group = None
        fp = open(file)
        for line in fp.readlines():
            line=line.rstrip('[\r\n]')
            if not name:
                m = self.rr.match(line)
                if m:
                    name=m.group(1)
                continue
            else:
                m = self.ra.match(line)
                if m:
                    group=m.group(1)
                    continue
                if self.re.match(line):
                    rule = self.makeRule(name,group,drool)
                    self.xmi.addDiagramClass(rule,diagram)
                    name=None
                    continue
                
        fp.close()
        return


    def makeRule(self,name,group,parent,prefix=None):
        rule = self.xmi.makeClass(name,parent)
        self.xmi.makeStereotype('Rule',self.string)
        if group:
            self.xmi.makeAttribute('group',None,group,rule)
        return rule

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
