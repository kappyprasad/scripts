#!/usr/bin/env python

import os,sys,re,json

import credstash

from Tools.argue import Argue
from _mysql import result

args = Argue()

@args.command(single=True)
class Squirrel(object):

    @args.attribute(short='v',flag=True)
    def verbose(self): return False

    @args.attribute(short='t')
    def table(self):
        '''
        the table name
        '''
        return 'auth0_credstash'
    
    @args.attribute(short='r')
    def region(self):
        '''
        define the AWS region
        '''
        return 'ap-southeast-2'

    @args.operation
    def get(self,name):
        '''
        get a KMS key

        '''
        return credstash.getSecret(name=name, region=self.region(), table=self.table())

    @args.operation
    def put(self,name,value):
        '''
        put a KMS name,value key

        '''
        return credstash.putSecret(name, value, region=self.region(), table=self.table())

    @args.operation
    def delete(self,name):
        '''
        delete a KMS name
        '''
        return credstash.deleteSecrets(name=name, region=self.region(), table=self.table())

    @args.operation
    def list(self):
        '''
        list the KMS names
        '''
        secrets = credstash.listSecrets(region=self.region(), table=self.table())
        return map(lambda x:x['name'], secrets)

    @args.operation(name="export")
    def exporter(self, _output):
        '''
        export the secrets in json name/value dict format
        
        :param _output: the output file in json
        :name  _output: output
        
        '''
        values = credstash.getAllSecrets(region=self.region(), table=self.table())
        with open(_output,'w') as fo:
            json.dump(values,fo,indent=4)
        return

    @args.operation(name="import")
    def importer(self, _input):
        '''
        import the secrets in json name/value dict format
        
        :param _input: input file in json
        :name  _input: input
        
        '''
        with open(_input) as fi:
            values=json.load(fi)
            for name in values.keys():
                print name
                self.put(name,values[name])
        return
    
if __name__ == '__main__':
    result = args.execute()
    if result:
        if type(result) == str:
            print result
        else:
            json.dump(result,sys.stdout,indent=4)


        
