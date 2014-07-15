#!/usr/bin/python

# $Date: 2014-06-04 16:05:55 +1000 (Wed, 04 Jun 2014) $
# $Revision: 11546 $
# $Author: david.edson $
# $HeadURL: http://cgu-svn/CGUBPMLombardi/trunk/Scripts/_tools/environments.py $
# $Id: environments.py 11546 2014-06-04 06:05:55Z david.edson $


import os,sys,re,pickle

from _tools.eddo import *
from _tools.xpath import *
from _tools.parser import *
from _tools.finder import *

class Environments:

    fname='%s/.env.map'%os.environ['HOME']

    p = re.compile('[^@]*@([^@]+)@.*')

    @property
    def map(self):
        return self.map

    @classmethod
    def __init__(self,cache=False, bpm=False):
        self.map = {}
        if cache:
            if os.path.isfile(self.fname):
                fp = open(self.fname)
                self.map = pickle.load(fp)
                fp.close()
                return

        self.keys = []
        svnurls = []

        if not 'SVN_MIDDLEWARE' in os.environ.keys():
            sys.exit('environment variable SVN_MIDDLEWARE not set')
        svnhome=os.environ['SVN_MIDDLEWARE']
        if not os.path.isdir(svnhome):
            sys.exit('SVN_MIDDLEWARE=%s directory doesn\'t exist'%svnhome)

        svnbases=[
            '%s/trunk/PCCellSetup'%svnhome,
            '%s/trunk/PSCellSetup'%svnhome
        ]
        if bpm:
            svnbases += [
                '%s/trunk/WCNSW_Application'%svnhome,
                '%s/trunk/WFC_Application'%svnhome,
                '%s/trunk/WM2_Application'%svnhome,
                '%s/trunk/BusinessServicesLayer'%svnhome
            ]

        for svnbase in svnbases:
            svnurls.append('%s/trunk/definitionfiles/environments'%svnbase)

        wasdefs = []
        for svnbase in svnbases:
            wasdir = '%s/trunk/wasdefs'%svnbase
            for file in findFiles(wasdir, fileOrDir=True, pn='^.*\.xml$'):
                wasdefs.append(file)

        (doc,ctx) = getContextFromString('<Environments/>')

        for svnurl in svnurls:
            for file in findFiles(svnurl,fileOrDir=True,pn='^.*\.xml$'):
                (d,c) = getContextFromFile(file)
                env = getElement(c,'/Environments/Environment')
                doc.getRootElement().addChild(env)
                self.map[env.prop('name')] = self.resolveSymbols(c,env)

        fp=open(self.fname,'w')
        pickle.dump(self.map,fp)
        fp.close()

        return

    @classmethod
    def printXML(self,xml,colour=True,output=sys.stdout):
        myParser = MyParser(colour=colour, rformat=True,output=output)
        myParser.parser.Parse(xml)
        del myParser
        return

    @classmethod
    def resolveSymbols(self,ctx,env):
        symbols = {}
        for symbol in getElement(ctx,'SymbolVars/SymbolVar',env):
            s1 = symbol.prop('name')
            if s1 and s1 not in self.keys:
                self.keys.append(s1)
            value = symbol.prop('value')

            while s1 and value:
                #print '%s=%s'%(s1,value)
                m = self.p.match(value)
                if m:
                    s2 = m.group(1)
                    r = symbols[s2]
                    #print '\t%s->%s'%(s2,r)
                    value = value.replace('@%s@'%s2,'%s'%r)
                else:
                    break

            symbols[s1] = value

        for target in getElement(ctx,'TargetHosts/TargetHost',env):
            key = target.prop('name')
            symbols[key] = target.prop('host')
            if key and key not in self.keys:
                self.keys.append(key)

        return symbols



