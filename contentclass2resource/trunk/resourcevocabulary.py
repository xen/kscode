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
"""Vocabulary containing the names of classes and their corresponding values
of the resource.

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.app.component.vocabulary import UtilityVocabulary, UtilityTerm
from zope.schema.vocabulary import SimpleTerm
from zope.app.component.vocabulary import UtilityNameTerm
from interfaces import IContentClassResource

class ResourceVocabulary(UtilityVocabulary):
    """Словарь, содержащий имена классов и соответствующие им значения ресурса,
    указанного в конструкторе как name"""

    def __init__(self, context, name=None, container=None, **kw):
        """Конструктор, отличающийся от обычного двумя дополнительными
        аргументами: name - это имя ресурса (поля IContentClassResource);
        container - это контейнер, в котором хранятся экземпляры
        IContentClassResource."""
        if name and container:
            self._terms = {}
            for key, item in container.items():
                if not IContentClassResource.providedBy(item):
                    continue
                s = getattr(item, name)
                self._terms[key] = SimpleTerm(key, token=key, title=s)
        else:
            raise u"Resource and container can't be empty!"
