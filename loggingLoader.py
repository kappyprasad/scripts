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
from sqlalchemy import \
    Column, \
    Integer, \
    String, \
    Float, \
    DateTime, \
    ForeignKey
from sqlalchemy.engine import \
    reflection
from sqlalchemy.orm import \
    relationship, \
    backref, \
    joinedload
from sqlalchemy.ext.declarative import \
    declarative_base
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
    parser.add_argument('-e', '--errors',   action='store_true', help='show pattern match errors')
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

    parser.add_argument('-T', '--dts',      action='store',      default='%Y-%m-%d %H:%M:%S')

    parser.add_argument('-g', '--regex',    action='store',      help='apply a s/regex/replace/ for each line before procesing')
    parser.add_argument('-G', '--replace',  action='store',      help='apply a s/regex/replace/ for each line before procesing')
    
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

    parser.add_argument('-s', '--server',   action='store',            default='localhost')
    
    group1=parser.add_mutually_exclusive_group(required=False)
    group1.add_argument('-i', '--input',    action='store', nargs='*')
    group1.add_argument('-q', '--query',    action='store_true')
                 

    args = parser.parse_args()
    if args.verbose: sys.stderr.write('args : %s' % vars(args))
    return args

####################################################################################################
@from_object()
@to_object()
class Server(Base):

    __tablename__ = 'server'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(50))

    def __init__(self,id=None,name=None):
        self.id=id
        self.name=name
        return
    
    def __dir__(self):
        return [
            'id',
            'name'
        ]

####################################################################################################
@from_object()
@to_object()
class Level(Base):

    __tablename__ = 'level'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(25))

    def __init__(self,id=None,name=None):
        self.id=id
        self.name=name
        return
    
    def __dir__(self):
        return [
            'id',
            'name'
        ]

####################################################################################################
@from_object()
@to_object()
class Key(Base):

    __tablename__ = 'key'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(255))

    def __init__(self,id=None,name=None):
        self.id=id
        self.name=name
        return
    
    def __dir__(self):
        return [
            'id',
            'name'
        ]

####################################################################################################
@from_object()
@to_object()
class File(Base):

    __tablename__ = 'file'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(255))
    loaded        = Column(Integer)
    
    def __init__(self,id=None,name=None,loaded=0):
        self.id=id
        self.name=name
        self.loaded=loaded
        return
    
    def __dir__(self):
        return [
            'id',
            'name',
            'loaded',
        ]

####################################################################################################
@from_object()
@to_object()
class Thread(Base):

    __tablename__ = 'thread'
    id            = Column(Integer, primary_key=True)
    name          = Column(String(255))

    def __init__(self,id=None,name=None):
        self.id=id
        self.name=name
        return
    
    def __dir__(self):
        return [
            'id',
            'name'
        ]


####################################################################################################
@from_object()
@to_object()
class Message(Base):

    __tablename__ = 'message'
    id            = Column(Integer, primary_key=True)
    server        = relationship(Server)
    server_id     = Column(Integer, ForeignKey('server.id'))
    file          = relationship(File)
    file_id       = Column(Integer, ForeignKey('file.id'))
    level         = relationship(Level)
    level_id      = Column(Integer, ForeignKey('level.id'))
    key           = relationship(Key)
    key_id        = Column(Integer, ForeignKey('key.id'))
    when          = Column(DateTime)
    thread        = relationship(Thread)
    thread_id     = Column(Integer, ForeignKey('thread.id'))
    description   = Column(String(4096))

    def __init__(
        self,
        id=None,
        server=None,
        file=None,
        when=None,
        level=None,
        thread=None,
        key=None,
        description=None
    ):
        self.id=id
        self.server=server
        self.file=file
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
            'server',
            'file',
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
def byName(tipe,name,session):
    value = None
    if tipe not in names.keys():
        names[tipe] = {}
    if name not in names[tipe].keys():
        value = session.query(tipe).filter_by(name=name).first()
        if not value:
            value = tipe(name=name)
            session.add(value)
            session.commit()
        names[tipe][name] = value
    return names[tipe][name]

####################################################################################################
def process(line,pattern,mapping,keys,session,server,file,dts,errors=False,regex=None,replace=None,verbose=False):
    if regex and replace:
        m = regex.match(line)
        if m:
            line = regex.sub(replace,line)
        #print line
    match = pattern.match(line)
    if not match:
        if errors:
            sys.stderr.write('%s\n'%line)
        return
    data = dict(server=byName(Server,server,session),file=file)
    for k in range(len(mapping)):
        value=match.group(k+1)
        if mapping[k] == 'when':
            data[mapping[k]] = datetime.strptime(value,dts)
        elif mapping[k] == 'thread':
            data[mapping[k]] = byName(Thread,value,session)
        elif mapping[k] == 'description':
            data[mapping[k]] = value
            for p in keys:
                m = p.match(value)
                if m:
                    data['key'] = byName(Key,m.group(1),session)
                    continue
        elif mapping[k] == 'level':
            data[mapping[k]] = byName(Level,value,session)
        else:
            data[mapping[k]] = value
    m = Message(**data)
    if verbose:
        print dumper(m)
    session.add(m)
    return
    
####################################################################################################
def main():
    global args, names
    args = argue()
    names = {}
    
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

    session = loader.Session()

    if args.test:
        file=byName(File,'test',session)
        for line in [
            '2016-05-20 09:20:58,056 [http-nio-8080-exec-5] INFO  Inserted: FlightEligibility',
            '2016-05-21 09:20:58,056 [http-nio-8080-exec-6] WARN  Inserted: FlightMucken',
        ]:
            process(
                line,pattern,mapping,keys,session,args.server,file,args.dts,args.errors,
                re.compile(args.regex) if args.regex else None,
                args.replace,
                args.verbose
            )
        file.loaded = 2
        session.commit()

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
        
        def load(input,server,file):
            fp = byName(File,file,session)
            loaded=fp.loaded
            for line in input.readlines()[loaded:]:
                process(
                    line,pattern,mapping,keys,session,server,fp,args.dts,args.errors,
                    re.compile(args.regex) if args.regex else None,
                    args.replace,
                    args.verbose
                )
                loaded+=1
                if loaded % args.window == 0:
                    fp.loaded = loaded
                    session.commit()
                    sys.stdout.write('%s -> %d\r'%(file,loaded))
                    sys.stdout.flush()
            sys.stdout.write('%s -> %d\n'%(file,loaded))
            fp.loaded=loaded
            session.commit()

        if args.input:
            for file in args.input:
                input = open(file)
                load(input,args.server,file)
                input.close()
        else:
            sys.stderr.write('\nreading from stdin ...\n')
            input = sys.stdin
            load(input,args.server,'stdin')
        
    session.close()
    
    del loader
    return

if __name__ == '__main__': main()
