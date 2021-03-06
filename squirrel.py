#!/usr/bin/env python

import os,sys,re,json,xmltodict

from Tools.argue import Argue
from Tools.Squirrel import Squirrel

args = Argue()

@args.command(single=True)
class SquirrelCommand(Squirrel):

    @args.attribute(short='v',flag=True)
    def verbose(self): return False

    def __init__(self):
        args.super(SquirrelCommand, self).__init__()
        return
    
    @args.operation
    def get(self,name):
        '''
        get a KMS key

        '''
        return args.super(SquirrelCommand, self).get(name)

    @args.operation
    def put(self,name,value):
        '''
        put a KMS name,value key

        '''
        return args.super(SquirrelCommand, self).put(name, value)

    @args.operation
    def delete(self,name):
        '''
        delete a KMS name
        '''
        return args.super(SquirrelCommand, self).delete(name)

    @args.operation
    def list(self):
        '''
        list the KMS names

        '''
        return args.super(SquirrelCommand,self).list()

if __name__ == '__main__':
    result = args.execute()
    if result:
        if type(result) in [str,unicode]:
            print result
        elif type(result) == list:
            print '\n'.join(result)
        else:
            json.dump(result,sys.stdout,indent=4)


        
