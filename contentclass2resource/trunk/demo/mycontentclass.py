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
"""The demo class for testing contentclass2resource package.

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import implements
from zope.app.container.contained import Contained
from persistent import Persistent
from interfaces import IMyContentClass, IDemoResource
from zope.schema import getFieldNames

class MyContentClass(Persistent, Contained):
    call = u''
    icon = u''
    implements(IMyContentClass, IDemoResource)
    def getData(self, *kv, **kw):
        return [(x, getattr(self, x)) for x in getFieldNames(IDemoResource)]
    def setData(self, data):
        pass
