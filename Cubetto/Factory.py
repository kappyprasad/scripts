#!/usr/bin/python

import sys, re, os, uuid, StringIO

from _tools.xmi import *
from _tools.parser import *
from _tools.xpath import *

import Cubetto

class Factory(object):

    __xmi     = None
    __indent  = False

    __engines = {}
    
    @property
    def xmi(self):
        return self.__xmi

    @xmi.setter
    def xmi(self,xmi):
        self.__xmi = xmi
        return

    @property
    def indent(self):
        return self.__indent

    @indent.setter
    def indent(self,indent):
        self.__indent = indent
        return
    
    @property
    def engines(self):
        return self.__engines

    @engines.setter
    def engines(self, engines):
        self.__engines = engines
        return

    def __init__(self, json, raw=False, indent=False):
        self.json = json
        self.xmi = XMI()
        self.indent = indent
        args = (json,self.xmi,raw)
        self.__engines = {
            'Project' : Cubetto.Project(*args),
            'ObjectType' : Cubetto.ObjectType(*args),
        }
        for key in self.__engines.keys():
            self.__engines[key].factory = self
        return
        
    def __del__(self):
        return

    def ingest(self):
        for key in self.engines.keys():
            self.engines[key].ingest()
        return

    def obtain(self, type=None, id=None):
        """
        find an aws entity by type and id
        @param type: Cubetto type
        @param id: string identity
        @return: (xmi,cubetto)
        """
        if type in self.engines.keys():
            return self.engines[type].obtain(id)
        return (None,None)

    def process(self):
        """
        relink any entity relationships
        """
        for key in self.engines.keys():
            self.engines[key].process()
        return

    def export(self,output):
        if self.indent:
            input = StringIO.StringIO('%s\n'%self.xmi.doc)
            doParse(False,False,True,input,False,output,False,True)
            input.close()
        else:
            output.write('%s\n'%self.xmi.doc)
        output.close()
        return
