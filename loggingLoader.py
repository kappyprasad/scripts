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

###############################################################################
def argue():
    parser = argparse.ArgumentParser(description='logging loader')
    
    parser.add_argument('-v', '--verbose',  action='store_true', help='show verbose detail')
    parser.add_argument('-c', '--colour',   action='store_true', help='colour output')
    parser.add_argument('-m', '--make',     action='store_true', help='make schema')
    parser.add_argument('-f', '--filter',   action='store',      help='filter_by')    
    parser.add_argument('-t', '--test',     action='store_true', help='insert test data')    
    parser.add_argument('-j', '--json',     action='store_true', help='output json')    
    parser.add_argument('-x', '--xml',      action='store_true', help='output xml')    
    
    parser.add_argument('-u', '--url',      action='store',      default='mysql+mysqlconnector://%s:%s@%s')
    parser.add_argument('-H', '--hostname', action='store',      default='localhost')
    parser.add_argument('-U', '--username', action='store',      default='root')
    parser.add_argument('-P', '--password', action='store',      default=None)
    parser.add_argument('-D', '--database', action='store',      default='logging')

    parser.add_argument('-r', '--regex',    action='store',      default='^(.*)$')
    parser.add_argument('log',              action='store',     nargs='*')
    
    args = parser.parse_args()
    if args.verbose: sys.stderr.write('args : %s' % vars(args))
    return args

###############################################################################
@from_object()
@to_object()
class Message(Base):

    __tablename__ = 'message'
    id            = Column(Integer, primary_key=True)
    when          = Column(DateTime)
    level         = Column(String(25))
    key           = Column(String(50))
    description   = Column(String(250))

    def __init__(self,id=None,when=None,level=None,key=None,description=None):
        self.id=id
        self.when=when
        self.level=level
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
            'key',
            'description',
        ]

##############################################################################
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

        
###############################################################################
def main():
    args = argue()

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
        session = loader.Session()
        m = Message(when=datetime.now(),level='INFO',key='k1',description='d1')
        session.add(m)
        session.commit()
        session.close()
 
    session = loader.Session()
   
    query = session.query(Message)
    if args.filter:
        fb={}
        for nvp in args.filter.split(','):
            (n,v) = nvp.split('=')
            fb[n]=v
        query = query.filter_by(fb)

    show(query.all())
        
    session.close()
    
    del loader
    return

if __name__ == '__main__': main()
