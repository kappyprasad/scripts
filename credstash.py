#!/usr/bin/env python

import os,sys,re,json

from Tools.argue import Argue
from Tools.credstash import CredStash

args = Argue()

@args.command(single=True)
class MyCredStash(CredStash):

    @args.attribute(short='r')
    def region(self):
        '''
        define the AWS region
        '''
        return args.super(MyCredStash,self).region()

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

if __name__ == '__main__':
    print args.execute()
    


        
