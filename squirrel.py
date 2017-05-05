#!/usr/bin/env python

import os,sys,re,json,xmltodict

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
    def list(self, _format=None):
        '''
        list the KMS names

        @args.parameter(
            param='_format',
            name='format',
            help='what type format do you want',
            short=True,
            flag=True,
            oneof={
                'json':'output as json',
                'xml' :'output as xml',
                'text':'output as text',
            },
            default='text'
        )
        '''
        secrets = [{'name':'value'}] #credstash.listSecrets(region=self.region(), table=self.table())

        print _format, type(_format)
        if _format == 'json':
            return secrets
        if _format == 'xml':
            return xmltodict.unparse({'items':{'item':secrets}}, indent=True)
        if _format == 'text':
            return '\n'.join(map(lambda x:x['name'], secrets))
        return
    
    @args.operation(name="export")
    def exporter(self, _output, _format=None):
        '''
        export the secrets in json name/value dict format
        
        @args.parameter(
            param='_output',
            name='output',
            help='the output file in json'
        )

        @args.parameter(
            param='_format',
            name='format',
            help='what type format do you want',
            short=True,
            oneof={
                'text':'output as text',
                'json':'output as json',
                'xml' :'output as xml'
            }
        )
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
        if type(result) in [str,unicode]:
            print result
        else:
            json.dump(result,sys.stdout,indent=4)


        
