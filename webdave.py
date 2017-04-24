#!/usr/bin/env python

import os,sys,re,json

from easywebdav import Client
from Tools.argue import Argue

args = Argue()

@args.command(single=True)
class WebDave(object):
    
    @args.attribute(short='H',default='localhost')
    def host(self): return
    
    @args.attribute(short='P',type=int,default=8080)
    def port(self): return
    
    def __init__(self):
        return
        
    @args.operation
    def ls(self,path):
        '''
        :param path: list this remote path
        '''
        return path
        
if __name__ == '__main__':
    results = args.execute()
    if results:
        json.dump(results,sys.stdout,indent=4)
