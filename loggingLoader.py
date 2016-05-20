#!/usr/bin/env python

import os, re, sys, argparse, json, uuid, xmltodict, logging

from datetime import datetime
from StringIO import StringIO

from jsonweb.encode import to_object,dumper
from jsonweb.decode import from_object,loader

from Tools.Passwords import *
from Alchemist.alloro import *
from Tools.pretty import *

import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref, joinedload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import \
    InstrumentedList, \
    InstrumentedDict, \
    InstrumentedSet, \
    attribute_mapped_collection

Base = declarative_base()

####################################################################################################
def argue():
    parser = argparse.ArgumentParser(description='logging loader')
    
    parser.add_argument('-v', '--verbose',  action='store_true', help='show verbose detail')
    parser.add_argument('-c', '--colour',   action='store_true', help='colour output')
    parser.add_argument('-m', '--make',     action='store_true', help='make schema')
    parser.add_argument('-w', '--window',   action='store',      type=int, default=1000)

    parser.add_argument('-f', '--filter',   action='store',      help='filter_by')
    parser.add_argument('-t', '--test',     action='store_true', help='insert test data')    
    parser.add_argument('-j', '--json',     action='store_true', help='output json')    
    parser.add_argument('-x', '--xml',      action='store_true', help='output xml')    

    parser.add_argument('-u', '--url',      action='store',      default='mysql+mysqlconnector://%s:%s@%s')
    parser.add_argument('-H', '--hostname', action='store',      default='localhost')
    parser.add_argument('-U', '--username', action='store',      default='root')
    parser.add_argument('-P', '--password', action='store',      default=None)
    parser.add_argument('-D', '--database', action='store',      default='logging')

    parser.add_argument('-r', '--pattern',  action='store',      default=\
                        '^'+
                        '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3}\s+'+
                        '\[([^\]]+)\]\s+'+
                        '(DEBUG|INFO|ERROR|WARN)\s+'+
                        '(.*)'+
                        '$'
    )
    parser.add_argument('-R', '--mapping',  action='store', nargs='*', default=[
                        'when',
                        'thread',
                        'level',
                        'description',
    ])

    parser.add_argument('-k', '--keys',     action='store', nargs='*', default=[
                        '^(Booking)\{.*$',
                        '^(Inserted):.*$',
                        '^(errai bus started).*',
                        '^(Repository :.*)$',
    ])
        
    group1=parser.add_mutually_exclusive_group(required=False)
    group1.add_argument('-i', '--input',    action='store')
    group1.add_argument('-q', '--query',    action='store_true')
                 

    args = parser.parse_args()
    if args.verbose: sys.stderr.write('args : %s' % vars(args))
    return args

####################################################################################################
@from_object()
@to_object()
class Message(Base):

    __tablename__ = 'message'
    id            = Column(Integer, primary_key=True)
    when          = Column(DateTime)
    level         = Column(String(25))
    thread        = Column(String(50))
    key           = Column(String(100))
    description   = Column(String(1024))

    def __init__(
        self,
        id=None,
        when=None,
        level=None,
        thread=None,
        key=None,
        description=None
    ):
        self.id=id
        self.when=when
        self.level=level
        self.thread=thread
        self.key=key
        self.description=description
        return
    
    def __initold__(self,*args,**kwargs):
        for k in kwargs.keys():
            if k in dir(self):
                setattr(self,k,getattr(kwargs,k))
        return
    
    def __dir__(self):
        return [
            'id',
            'when',
            'level',
            'thread',
            'key',
            'description',
        ]

####################################################################################################
class Loader(object):

    def __init__(self,args,password):
        url = args.url%(
            args.username,
            password,
            args.hostname
        )

        print url
        
        if args.make:
            engine = sqlalchemy.create_engine(url)
            for dbr in engine.execute('show databases'):
                if '%s'%dbr[0] == args.database:
                    sys.stderr.write('dropping %s\n'%args.database)
                    engine.execute('drop database %s'%args.database)
            sys.stderr.write('creating %s\n'%args.database) 
            engine.execute('create database %s'%args.database)
            engine.execute('use %s'%args.database)
            del engine
            
        self.engine = sqlalchemy.create_engine(
            '%s/%s'%(
                url,
                args.database
            ),
            echo=args.verbose
        )

        if args.make:
            Base.metadata.create_all(self.engine)

        self.Session = sqlalchemy.orm.sessionmaker()
        self.Session.configure(bind=self.engine)
        return

####################################################################################################
def process(line,pattern,mapping,keys,session):
    match = pattern.match(line)
    if not match:
        #sys.stderr.write('%s\n'%line)
        return
    data = dict()
    for k in range(len(mapping)):
        value=match.group(k+1)
        if mapping[k] == 'when':
            value = datetime.strptime(value,"%Y-%m-%d %H:%M:%S")
        if mapping[k] == 'description':
            for p in keys:
                m = p.match(value)
                if m:
                    data['key'] = m.group(1)
                    continue
        data[mapping[k]] = value
    m = Message(**data)
    #print dumper(m)
    session.add(m)
    return
    
####################################################################################################
def main():
    args = argue()

    pattern = re.compile(args.pattern)
    #print pattern.pattern
    mapping = args.mapping
    #print mapping
    keys = map(lambda x:re.compile(x),args.keys)
    
    def show(o):
        if args.json:
            print dumper(o,exclude_nulls=False,indent=4)
    
        if args.xml:
            alloro(o,Base=Base,colour=args.colour,output=sys.stdout)
    
    level=logging.INFO
    if args.verbose:
        level=logging.DEBUG
        
    logging.basicConfig(level=level)
    
    if args.password:
        password=args.password
    else:
        password=Passwords(args.hostname, args.database, args.username).password

    loader = Loader(args,password)

    if args.test:
        line = '2016-05-20 09:20:58,056 [http-nio-8080-exec-5] INFO  Inserted: FlightEligibility'
        session = loader.Session()
        process(line,pattern,mapping,keys,session)
        session.commit()
        session.close()
        return
    
    if args.input:
        input = open(args.input)
    else:
        input = sys.stdin
        
    session = loader.Session()

    if args.query:
        query = session.query(Message)
        if args.filter:
            fb={}
            for nvp in args.filter.split(','):
                (n,v) = nvp.split('=')
                fb[n]=v
            query = query.filter_by(fb)

        show(query.all())
    else:
        window=0
        for line in input.readlines():
            process(line,pattern,mapping,keys,session)
            window+=1
            if window % args.window == 0:
                session.commit()
                sys.stdout.write('%d\r'%window)
                sys.stdout.flush()
        session.commit()
        sys.stdout.write('\n')

    if args.input:
        input.close()
        
    session.close()
    
    del loader
    return

if __name__ == '__main__': main()
