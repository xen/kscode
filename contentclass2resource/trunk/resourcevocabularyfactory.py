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
"""Factory for ResourceVocabulary

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import implements
from persistent import Persistent
from zope.app.container.contained import Contained
from zope.schema.interfaces import IVocabularyFactory
from resourcevocabulary import ResourceVocabulary

class ResourceVocabularyFactory(Persistent, Contained):
    """Фабрика для ResourceVocabulary"""
    implements(IVocabularyFactory)

    def __init__(self, name=None, *kv, **kw):
        super(ResourceVocabularyFactory, self).__init__(self, *kv, **kw)
        self.name = name

    def __call__(self, context):
        container = self.__parent__.__parent__
        return ResourceVocabulary(context,
                                  name=self.name,
                                  container=container)
