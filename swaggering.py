#!/usr/bin/env python

import os, sys, re, xmltodict, json, yaml, argparse, logging

from swagger_parser import SwaggerParser

from Tools.argue import Argue

args = Argue()

#_____________________________________________________________
@args.command(single=True)
class Swaggering(object):

    @args.attribute(short='i')
    def input(self): return
    
    @args.attribute(short='o')
    def output(self): return 
    
    def __init__(self):
        self.parser = SwaggerParser(swagger_path=self.input())
        if self.output():
            self._output = open(self.output(),'w')
        else:
            self._output = sys.stdout

    def __del__(self):    
        if self.output():
            self._output.close()
          
    @args.operation
    def paths(self):
        for path in self.parser.paths:
            self._output.write('%s\n'%path)
        return
    
    @args.operation
    def spec(self,path):
        '''
        show the path spec

        :param path: the path

        '''
        return self.parser.get_path_spec(path)
        
#_____________________________________________________________
if __name__ == '__main__': 
    results = args.execute()
    if results:
        json.dumps(results,sys.stdout,indent=4)
        
