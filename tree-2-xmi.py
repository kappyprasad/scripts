#!/usr/bin/python




####################################################################################
import sys,re,os,argparse

from subprocess import Popen, PIPE

from _tools.xmi import *
from _tools.xpath import *
from _tools.parser import *
from _tools.pretty import *
from _tools.finder import *

####################################################################################
parser = argparse.ArgumentParser()

fgroup = parser.add_mutually_exclusive_group()
fgroup.add_argument('-l','--link',    action='store_true', help='link local files')
fgroup.add_argument('-s','--svn',     action='store_true', help='link svn files')

parser.add_argument('-v','--verbose', action='store_true', help='show help')
parser.add_argument('-o','--output',  action='store',      help='output.xmi file name', default='.xmi')
parser.add_argument('dir',            action='store',      help='the directory')

args = parser.parse_args()

####################################################################################
if args.verbose:
    prettyPrint(vars(args),colour=True,output=sys.stderr)
    sys.stderr.flush()

if args.svn:
    process = Popen('svn info --xml %s'%args.dir,shell=True,stdout=PIPE)
    (sdoc,sctx) = getContextFromString(''.join(map(lambda x : x.rstrip(), process.stdout.readlines())))
    del process
    svn=getElementText(sctx,'/info/entry/url')
    if args.verbose: 
        sys.stderr.write('svn=%s\n'%svn)
        sys.stderr.flush()

####################################################################################
def concatPath(prefix,suffix):
    path = suffix
    if prefix:
        path = '%s/%s'%(prefix.rstrip('/'),suffix)
    return path

####################################################################################
class DirectoryTree:

    @property
    def doc(self):
        return self.xmi.doc

    def __init__(self,xmi=XMI()):
        self.xmi = xmi

    def makeDirectory(self,name,parent=None,prefix=None):
        if parent == None:
            parent = self.xmi.modelNS
        element = self.xmi.makePackage(name,parent)
        dir = concatPath(prefix,name)
        for f in os.listdir(dir):
            fp = concatPath(dir,f)
            if args.verbose:
                sys.stderr.write('< %s\n'%fp)
                sys.stderr.flush()
            if os.path.isfile(fp):
                self.makeFile(f,element,dir)
            elif os.path.isdir(fp):
                self.makeDirectory(f,element,dir)
        return


    def makeFile(self,name,parent,prefix=None):
        classCF = self.xmi.makeClass(name,parent)
        fp = os.path.abspath(concatPath(prefix,name))
        p = re.compile('^/cygdrive/([a-z])(/.*)$')
        m = p.match(fp)
        if m:
            fp = '%s:%s'%m.groups()
        if fp[0] == '/':
            fp = 'c:/cygwin%s'%fp
        fp = fp.replace('/','\\')
        self.xmi.makeEAFile(fp,'Local File',classCF.parent)
        return

####################################################################################
def main():
    global files
    
    dt = DirectoryTree()
    dt.makeDirectory(args.dir)

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
