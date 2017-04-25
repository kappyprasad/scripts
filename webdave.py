#!/usr/bin/env python

import os,sys,re,json
import keychain,x_callback_url

from threading import Event
from time import sleep
from datetime import datetime
from requests.auth import HTTPDigestAuth
from easywebdav import Client
from Tools.argue import Argue

app = 'workingcopy'
usr = 'x-callback-key'
key = keychain.get_password(app,usr)

dts = '%Y-%m-%d %H:%M:%S'
lock = '.webdave'

args = Argue()

@args.command(single=True)
class WebDave(object):

    @args.attribute(short='H',default='localhost')
    def host(self): return
    
    @args.attribute(short='P',type=int,default=8080)
    def port(self): return
    
    @args.attribute(short='u',default='webdav')
    def username(self): return
    
    @args.attribute(short='p')
    def password(self): return key
    
    def __init__(self):
        self.client =Client(
            host=self.host(),
            port=self.port(),
            auth=HTTPDigestAuth(
                self.username(),
                self.password()
            )
        )
        return
    
    @args.operation
    def start(self):
        data = { 'key' : key, 'cmd' : 'start' }
        
        url='working-copy://x-callback-url/webdav/%s'%x_callback_url.params(data)
        
        def itemsHandler(parameters):
            print json.dumps(parameters,indent=4)

        x_callback_url.open_url(url,itemsHandler)
        return
              
    @args.operation
    def ls(self,paths,all=False,long=False):
        '''
        :param paths: list these remote paths
        :nargs paths: *
        
        :param all  : ls all files
        :flag  all  : True
        
        :param long : show details
        :flag  long : True
        
        '''
        l = list()
        for path in paths or ['.']:
            l = l + self.client.ls(path)
        return l
        
if __name__ == '__main__':
    results = args.execute()
    if results:
        json.dump(results,sys.stdout,indent=4)
