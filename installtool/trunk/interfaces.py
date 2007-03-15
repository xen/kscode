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
"""Interfaces for the Zope 3 based <> package

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface
from zope.schema import TextLine, Field

class IScriptError(Interface):

    script = TextLine(title=u'Script name', required=False)
    
    msg = TextLine(title=u'Error message', required=False)
    
    res = Field()

class IUnresolvedDepsError(Interface):
    """Интерфейс для исключения, возбуждаемого при невозможности разрешить
    зависимости. Имеет дополнительный параметр res, содержащий список скриптов
    для которых не удалось разрешить зависимости."""
    
    res = Field()

class IUnknownDependencyError(Interface):
    """Интерфейс для исключения, возбуждаемого при нахождении несуществующей
    зависимости. Имеет дополнительные параметр msg содержащие сообщение об
    имени скрипта, содержащего неизвестную зависимость и имени этой
    зависимости."""
    
    msg = TextLine(title=u'Error message', required=False)
