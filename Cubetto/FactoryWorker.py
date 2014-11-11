#!/usr/bin/python

import Cubetto

class FactoryWorker(object):
    
    __json       = None
    __factory    = None
    __name       = None
    __xmi        = None
    __raw        = False
    __package    = None
    __diagram    = None

    @property
    def json(self):
        return self.__json
    
    @property
    def factory(self):
        return self.__factory

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name
        return

    @factory.setter
    def factory(self,factory):
        self.__factory = factory
        return

    @property
    def xmi(self):
        return self.__xmi

    @xmi.setter
    def xmi(self,xmi):
        self.__xmi = xmi
        return

    @property
    def raw(self):
        return self.__raw

    @raw.setter
    def raw(self, raw):
        self.__raw = raw
        return

    @property
    def package(self):
        return self.__package

    @package.setter
    def package(self,package):
        self.__package = package
        return

    @property
    def diagram(self):
        return self.__diagram

    @diagram.setter
    def diagram(self,diagram):
        self.__diagram = diagram
        return

    def __init__(self, json, xmi, raw=False):
        self.__json = json
        self.xmi = xmi
        self.raw = raw
        self.entities = {}
        return

    def ingest(self):
        """ please implement this worker method"""
        raise NotImplementedError()

    def obtain(self, id=None):
        """
        please implement this worker method
        @param id: entity id
        @return: (xmi,aws) the element
        """
        raise NotImplementedError()

    def process(self):
        """
        relink any entity relationships
        """
        raise NotImplementedError()


