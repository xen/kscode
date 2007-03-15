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
"""Container storage for content-class resources.

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import implements
from zope.app.container.btree import BTreeContainer
from interfaces import IResourceContainer, IContentClassResource
from resourcevocabularyfactory import ResourceVocabularyFactory
from zope.schema import getFieldNames
from zope.schema.interfaces import IVocabularyFactory
from zope.app import zapi

class ResourceContainer(BTreeContainer):
    """Реализация контейнера для ресурсов контент-класса"""
    implements(IResourceContainer)
    prefix = u'rescon_'
    vocabularies = None

    def __init__(self, *kv, **kw):
        """Создаёт контейнер, в котором хранятся фабрики словарей"""
        super(ResourceContainer, self).__init__()
        self.vocabularies = BTreeContainer()
        self.vocabularies.__parent__ = self
    
    def regenerateVocabularies(self):
        """Создаёт/пересоздаёт и регистрирует словари, каждый из которых
        соответствует определённому полю IContentClassResource"""
        self.unregisterVocabularies()
        lst = [x for x in self.vocabularies.keys()]
        if lst:
            for x in lst:
                del(self.vocabularies[x])
        lst = getFieldNames(IContentClassResource)
        for x in lst:
            name = '%s%s' % (self.prefix, x)
            self.vocabularies[name] = ResourceVocabularyFactory(name=x)
        self.registerVocabularies()

    def registerVocabularies(self):
        """Registers all created factories"""
        siteman = zapi.getSiteManager()
        for key, value in self.vocabularies.items():
            siteman.registerUtility(value,
                                    provided=IVocabularyFactory,
                                    name=key)

    def unregisterVocabularies(self):
        """Unregisters all created factories"""
        siteman = zapi.getSiteManager()
        for key, value in self.vocabularies.items():
            siteman.unregisterUtility(value,
                                      provided=IVocabularyFactory,
                                      name=key)
