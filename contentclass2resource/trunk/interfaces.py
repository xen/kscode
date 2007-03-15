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
"""Interfaces for the Zope 3 based contentclass2resource package

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.schema import TextLine, Choice, Field
from zope.app.container.interfaces import IContainer, IContained
from zope.app.container.constraints import ItemTypePrecondition
from zope.app.container.constraints import ContainerTypesConstraint
from zope.schema.interfaces import IVocabularyFactory

class IContentClassResource(Interface):
    """Интерфейс для набора ресурсов контент-класса"""
    call = TextLine(
        title=u'Class name',
        description=u'Russian class name',
        default=u'',
        required=True)
    icon = TextLine(
        title=u'Class icon',
        description=u'Name of class icon',
        default=u'',
        required=True)

class IContentClassResourceSchema(IContentClassResource):
    """Дополнительный интерфейс, по которому создаётся схема для форм добавления
    и редактирования"""
    name__ = Choice(
        title=u'Content name',
        description=u'Name class for resource',
        vocabulary='ContentNames',
        required=True)

class IResourceContainer(IContainer):
    """Контейнер, содержащий набор ресурсов. Ресурс имеет имя, совпадающее с
    именем класса и набор полей, соответствующих параметрам класса. Для каждого
    класса существует одинаковый набор ресурсов."""
    prefix = TextLine(
        title=u'Prefix',
        description=u'Prefix for vocabulary name',
        default=u'rescon_',
        required=True)
    vocabularies = Field()
    def regenerateVocabularies(self):
        """Создаёт/пересоздаёт и регистрирует словари ресурсов"""
        pass
    def registerVocabularies():
        """Регистрирует ранее созданные словари ресурсов"""
        pass
    def unregisterVocabularies():
        """Снимает регистрацию со словарей ресурсов"""
        pass
    def __setitem__(name, obj):
        pass
    __setitem__.precondition = ItemTypePrecondition(IContentClassResource)

class IContentClassResourceContained(IContained):
    __parent__ = Field(constraint=ContainerTypesConstraint(IResourceContainer))
