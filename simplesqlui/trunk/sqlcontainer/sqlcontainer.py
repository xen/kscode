### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/) 
# Все права защищены, 2006-2007 
#
# Developed by Key Solutions (http://keysolutions.ru/)                             
# All right reserved, 2006-2007                                   
#######################################################################
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################
"""RecordBase class for the Zope 3 based record package

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.app import zapi
from zope.app import zapi
from zope.interface import implements
from zope.component import ComponentLookupError
from interfaces import ISqlContainer
from zope.publisher.interfaces import NotFound
from sys import _getframe
from simplesqlui.factory.interfaces import ISqlFactory

class SqlContainerBase(object) :
    """Base record class"""
    
    implements(ISqlContainer)

    rfs = None
    
    def __init__(self,**kw):
        super(SqlContainerBase,self).__init__(**kw)
    
    def __getitem__(self,key) :
        "See zope.interface.common.mapping.IItemMapping"
        try:
            rf,key = key.split("=")
        except ValueError :
            raise KeyError
            
        try :
            ob = getattr(self,rf).get(key,self)        
        except AttributeError :
            raise KeyError
        ob.__name__ = rf + "=" +  ob.__name__
        return ob

    def get(self, key, default=None):
        "See zope.interface.common.mapping.IReadMapping"
        try:
            rf,key = key.split("=")
        except ValueError :
            return default

        ob = getattr(self,rf).get(key,self)
        ob.__name__ = rf + "=" +  ob.__name__
        return ob

    def keys(self):
        "See zope.interface.common.mapping.IEnumerableMapping"
        for rf in self.rfs :
            for (x,y) in  getattr(self,rf).items(self) :
                yield rf+"="+x

    def __iter__(self):
        "See zope.interface.common.mapping.IEnumerableMapping"
        for rf in self.rfs :
            for (x,y) in  getattr(self,rf).items(self) :
                yield rf+"="+x

    def values(self):
        "See zope.interface.common.mapping.IEnumerableMapping"
        for rf in self.rfs :
            for (x,y) in  getattr(self,rf).items(self) :
                y.__name__ = rf + "=" + y.__name__
                yield y

    def items(self):
        "See zope.interface.common.mapping.IEnumerableMapping"
        for rf in self.rfs :
            for (x,y) in  getattr(self,rf).items(self) :
                y.__name__ = rf + "=" + y.__name__
                yield (rf+"="+x,y)

    def __len__(self):
        "See zope.interface.common.mapping.IEnumerableMapping"
        return len(tuple(self.items()))

    def __contains__(self, key):
        "See zope.interface.common.mapping.IReadMapping"
        try :
            self.get(key,self)
        except Exception :
            return False
        return True

    def __delitem__(self, name):
        "See zope.app.container.interfaces.IWriteContainer"
        # TODO
        
    def __setitem__(self, name, object):
        "See simplesqlui.record.interfaces.ISqlContainer"
        if not self.__contains__(name) :
            raise RuntimeError

    def add(self,ob) :
        for rf in self.rfs :
            rfo = getattr(self,rf)
            if isinstance(ob,rfo.recordClass) :
                break
        else :
            raise RuntimeError                
    
        ob.register(self,"",rfo.ds,rfo.ids)
        return rf + "=" + rfo.add(ob)


class SqlJoin(property):
    """attribute that used as join beetween RecordBase objects"""
    
    def __init__(self, name):
        super(SqlJoin, self).__init__(self.get, self.set)
        self.name = name
        
    def get(self,ob) :
        return zapi.getUtility(ISqlFactory, self.name)
    
    def set(self, ob, value):
        raise RuntimeError
    

def sqljoin(name) :
    ns = _getframe(1).f_locals
    ns[name] = SqlJoin(name)
    ns.setdefault('rfs',[]).append(name)
