#!/usr/bin/env python

import os,sys,re,json

from Tools.argue import Argue
from Tools.credstash import CredStash

args = Argue()

@args.command(single=True)
class MyCredStash(CredStash):

    @args.attribute(short='v',flag=True)
    def verbose(self): return False

    @args.attribute(short='t')
    def table(self):
        '''
        the table name
        '''
        return args.super(MyCredStash,self).table()
    
    @args.attribute(short='r')
    def region(self):
        '''
        define the AWS region
        '''
        return args.super(MyCredStash,self).region()

    @args.operation
    def setup(self):
        '''
        call the setup for credstash
        '''
        return args.super(MyCredStash,self).setup()
    
    @args.operation
    def get(self,name):
        '''
        get a KMS key

        '''
        return args.super(MyCredStash,self).get(name)

    @args.operation
    def put(self,name,value):
        '''
        put a KMS name,value key

        '''
        return args.super(MyCredStash,self).put(name,value)

    @args.operation
    def delete(self,name):
        '''
        delete a KMS name
        '''
        return args.super(MyCredStash,self).delete(name)

    @args.operation
    def list(self):
        '''
        list the KMS names
        '''
        return '\n'.join(args.super(MyCredStash,self).list())

    @args.operation(name="export")
    def exporter(self, output):
        values=dict()
        for name in self.list().split('\n'):
            print name
            values[name]=self.get(name)
        with open(output,'w') as fo:
            json.dump(values,fo,indent=4)
        return

    @args.operation(name="import")
    def importer(self,input):
        with open(input) as fi:
            values=json.load(fi)
            for name in values.keys():
                print name
                self.put(name,values[name])
        return
    
if __name__ == '__main__':
    result = args.execute()
    if result:
        print result
    


        
