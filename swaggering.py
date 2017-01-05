#!/usr/bin/env python

import os, sys, re, xmltodict, json, yaml, argparse, logging

from swagger_parser import SwaggerParser

from Tools.argue import Argue

args = Argue()

def argue():
    parser = argparse.ArgumentParser()

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('-x', '--xml',       action='store_true',  help='xml output')
    group1.add_argument('-j', '--json',      action='store_true',  help='json output')
    group1.add_argument('-y', '--yaml',      action='store_true',  help='yaml output')
    
    return args


@args.command(name='swagger')
class Swaggering(object):
    
    @args.function(short='o')
    def output(self): return 
    
    def __init__(self):
        if self.output():
            self._output = open(self.output(),'w')
        else:
            self._output = sys.stdout

    def __del__(self):    
        if self.output():
            self._output.close()
          
    @args.operation
    def paths(self, path):                    
        self.parser = SwaggerParser(swagger_path=path)
        for path in self.parser.paths:
            self._output.write('%s\n'%path)
        return
    
if __name__ == '__main__': args.execute()
