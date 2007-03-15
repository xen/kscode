## -*- coding: utf-8 -*- #############################################
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
"""Factory class for the Zope 3 based factory package

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.app import zapi
from zope.interface import Interface
from persistent import Persistent
from zope.interface import implements
from zope.app.container.contained import Contained


from interfaces import ISqlFactory, ISqlFactoryProp
from simplesqlui.record.interfaces import IRecordBase
from simplesqlui.ds.interfaces import IDS
from simplesqlui.ds.ds import NullDS
from simplesqlui.mountpoint.interfaces import IMountpoint

class Factory(Persistent, Contained) :
    """"The Factory class"""
    
    implements(ISqlFactory, ISqlFactoryProp)
    
    datasource = None
    ids = ()
    factory = ""
    
    def __init__(self):
        pass
    
    @property
    def ds(self):
        if self.datasource is not None :
            return zapi.getUtility(IDS, self.datasource)
        return NullDS()

    @property
    def recordClass(self) :
        return zapi.getUtility(IRecordBase, self.factory, context=self)        
    
    @property
    def recordFactory(self):
        return lambda record, **kw: self.recordClass(**kw).register(record,self.joinkey(kw),self.ds,self.ids)
    
    def splitkey(self, key) :
        ids = key.split(".")        
        if len(self.ids) != len(ids) :
            raise KeyError,key
        return dict(zip(map(str,self.ids),ids))    
        
    def joinkey(self,d) :
        return ".".join([str(d[x]) for x in self.ids])
      
    def items(self,record) :
        for item in self.ds.select_all(**record.dict) :
            name = self.joinkey(item)
            yield (name ,self.recordFactory(record,**item))
            
    def get(self,key,record) :
        return self.recordFactory(record,
             **self.ds.select(
                **dict( record.dict.items()+ self.splitkey(key).items() )
             ) )
                 
    def add(self,record) :
        ld = []
        ob = record.__parent__

        while not IMountpoint.providedBy(ob) :
            ld.append( dict([(str(x),getattr(ob,x)) for x in ob.ids] ) )    
            ob = ob.__parent__
            
        ld.append(ob.dict)

        ld.reverse()
        rd = {}
        for d in ld :
            rd.update(d)

        rd.update(record.dict)    
        return self.joinkey( 
          self.ds.insert(
                  **rd       
          )  )
