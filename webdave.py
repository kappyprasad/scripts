#!/usr/bin/env python

import os,sys,re,json
import console,keychain,x_callback_url

from datetime import datetime
from requests.auth import HTTPDigestAuth
from easywebdav import Client, aest
from Tools.argue import Argue

app = 'workingcopy'
usr = 'x-callback-key'
key = keychain.get_password(app,usr)

dts = '%Y-%m-%d %H:%M:%S'

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
            
        if long:
            fmt = '{:<30} {:>7} {:<20}'
            for i in range(len(l)):
                t = l[i].mtime
                if t != '':
                    t = aest(t).strftime(dts)
                l[i] = fmt.format(
                    l[i].name,
                    l[i].size,
                    t
                )
        else:
            l = map(lambda x:x.name, l)
            
        print '\n'.join(l)
        return
        
if __name__ == '__main__':
    console.clear()
    data = { 'key' : key, 'cmd' : 'start' }
    
    url='working-copy://x-callback-url/webdav/%s'%x_callback_url.params(data)
    
    def callback(parameters):
        args.execute()
        
    x_callback_url.open_url(url,callback)
    
    

