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
"""MountPoint class for the Zope 3 based mountpoint package

$Id$
"""
__author__  = ""
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.app import zapi
from zope.interface import Interface
from persistent import Persistent
from zope.interface import implements
from zope.app.container.contained import Contained
                
from interfaces import IMountpoint

from simplesqlui.factory.interfaces import ISqlFactory
from simplesqlui.ds.interfaces import IDS
from simplesqlui.sqlcontainer.interfaces import ISqlContainer
from simplesqlui.sqlcontainer.sqlcontainer import SqlContainerBase
from simplesqlui.ds.ds import NullDS

class MountPoint(SqlContainerBase, Persistent, Contained) :
    """The mountpoint class"""
    
    implements(IMountpoint)

    datasource = None
    factory = ""
    dict = {}
    rfs=['rf']
    
    def __init__(self,datasource=None, factory=None) :
        self.datasource = datasource
        self.factory = factory
            
    @property
    def ds(self):
        if self.datasource is None :
            return NullDS()
        return zapi.getUtility(IDS, self.datasource)
    
    @property
    def rf(self):
        return zapi.getUtility(ISqlFactory, self.factory)

    def setDict(self,value) :
        self.dict = dict([(str(x),y) for (x,y) in [x.split() for x in value]])

    def getDict(self) :
        return [("%s %s" % (x,y)) for (x,y) in self.dict.items()]
        
    dict_ = property(getDict,setDict)
    
    @property
    def ids(self) :
        return self.dict.keys()
        