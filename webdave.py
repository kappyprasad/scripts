#!/usr/bin/env python

import os,sys,re,json,requests
import console,keychain,x_callback_url

from datetime import datetime
from requests.auth import HTTPDigestAuth
from easywebdav import Client, aest
from Tools.argue import Argue

app = 'workingcopy'
usr = 'x-callback-key'
key = keychain.get_password(app,usr)

dts = '%Y-%m-%d %H:%M:%S'
fmt = '{:<20} {:>7} {}'
       
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
    def ls(self,paths,all=False,long=False):
        '''
        :param paths: list these remote paths
        :nargs paths: *
        
        :param all  : ls all files
        :short all  : s
        :flag  all  : True
        
        :param long : show details
        :short long : l
        :flag  long : True
        
        '''
        l = list()
        for path in paths or ['.']:
            l = l + self.client.ls(path)
      
        for f in l:  
            if f.isdir:
                console.set_color(0,1,1)
            else:
                console.set_color(1,1,0)
            if long:
                t = f.mtime
                if t != '':
                    t = aest(t).strftime(dts)
                print fmt.format(t,f.size,f.name)
            else:
                print f.name
                
            console.set_color(1,1,1)
            
        return
        
if __name__ == '__main__':
    console.clear()
    console.set_font('Menlo',10)
    
    def callback(parameters):
        args.execute()  
    try:
        callback(None)
    except requests.exceptions.ConnectionError:
        print sys.exc_info()
        data = { 'key' : key, 'cmd' : 'start' }
        url='working-copy://x-callback-url/webdav/%s'%x_callback_url.params(data)  
        x_callback_url.open_url(url,callback)
        
    

