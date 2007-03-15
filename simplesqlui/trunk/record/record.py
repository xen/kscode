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
from zope.interface import implements
from zope.component import ComponentLookupError
from sys import _getframe
from transaction.interfaces import ITransactionManager
from transaction._manager import TransactionManager
import transaction
from interfaces import IRecordBase,IRecordContained
from zope.app.container.contained import Contained

class RecordBase(Contained) :
    """Base record class"""
    
    implements(IRecordBase,IRecordContained)
    
    __parent__ = None
    __name__ = None
    ds = None
    ids = []
    
    def __init__(self, **kw):
        self.dict = kw.copy()

    def register(self, __parent__, __name__, ds, ids) :
        self.__parent__ = __parent__
        self.__name__ = __name__
        self.ds = ds
        self.ids = ids[:]
        return self
    
    def commit(self) :
        """update all fields"""
        
        if self.ds :
            self.ds.update(**self.dict)
        
class SqlAttribute(property):
    """attribute that used within RecordBase objects"""
    
    def __init__(self, name):
        super(SqlAttribute, self).__init__(self.get, self.set)
        self.name = name
        
    def get(self,ob) :
        try:
            return ob.dict[self.name]
        except KeyError:
            try :
                ob.dict.update( ob.ds.select(**ob.dict) )
            except IndexError,msg :
                raise RuntimeError,msg
        return ob.dict[self.name]
    
    def set(self, ob, value):
        ob.dict[self.name] = value
        if ob.ds :
            txn=transaction.get()
            txn.addBeforeCommitHook(ob.commit)
    

def sqlattribute(name) :
    ns = _getframe(1).f_locals
    ns[name] = SqlAttribute(name)

