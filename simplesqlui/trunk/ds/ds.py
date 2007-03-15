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
"""DS class for the Zope 3 based ds package

$Id$
"""
__author__  = "Arvid, Andrey Orlov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from zope.app import zapi
                
from interfaces import IDS

def row2dict(row) :
    return dict([ (x,getattr(row,x)) for x in row.__slots__ ])


class DS(BTreeContainer) :
    """The DataSource class"""
    
    implements(IDS)
    
    def __init__(self):
        super(DS, self).__init__()
    
    def select(self, **kw):
        """use select sql script"""
        record = self["select"](**kw)
        if record:
            return row2dict(record[0])
        else:
            raise KeyError
        
    def select_all(self,**kw):
        """use select_all sql script"""
        return (row2dict(x) for x in self["select_all"](**kw))
        
    def update(self, **kw):
        """use update sql script"""
        self["update"](**kw)
        
    def delete(self, **kw):
        """use delete sql script"""
        self["delete"](**kw)
        
    def insert(self,**kw) :
        """user insert sql script"""
        return row2dict(self["insert"](**kw)[0])
                
class NullDS(object) :
    """The Null DataSource class"""
    
    implements(IDS)
    
    def select(self, **kw):
        raise KeyError
        
    def select_all(self):
        """use select_all sql script"""
        return []
        
    def update(self, **kw):
        """use update sql script"""
        return None
        
    def delete(self, **kw):
        """use delete sql script"""
        return None
    
    def insert(self,**kw) :
        """user insert sql script"""
        return ""
        