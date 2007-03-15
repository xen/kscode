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
"""Interfaces for the Zope 3 based interfaceswitcher package

$Id$
"""
__author__  = "Anatoly Zaretsky"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__    = "$Date$"
 
from zope.interface import Interface
from zope.schema import Choice


class IInterfaceSwitcherAble(Interface):
    'Switching ability marker'
    pass

class ISwitchableSchema(Interface):
    marker = Choice(
        title=u"Switchable marker",
        vocabulary="InterfaceSwitcherVocabulary")
