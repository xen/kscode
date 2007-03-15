### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/)    
# Все права защищены, 2006-2007                                       
#                                                                     
# Developed by Key Solutions (http://keysolutions.ru/)                
# All rights reserved, 2006-2007                                      
#######################################################################
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################
"""The interfaceSwitcherVocabulary factory

$Id$ """ 

__author__  = "Andrey Orlov, 2007 02 03" 
__license__	= "ZPL" 
__version   = "$Revision$" 
__date__    = "$Date$"


from zope.schema.vocabulary import SimpleVocabulary
from zope.app.zapi import getUtilitiesFor
from zope.interface.interfaces import IInterface
from zope.interface import implementedBy
from zope.proxy import getProxiedObject

from interfaceswitcher.interfaces import IInterfaceSwitcherAble


def interfaceSwitcherVocabulary(context):
    """Get utitlity vocabulary for IInterfaceSwitcher"""
    obj = getProxiedObject(context)
    for iface in implementedBy(obj.__class__):
        if iface.extends(IInterfaceSwitcherAble):
            items = (marker for marker in getUtilitiesFor(IInterface, context)
                            if marker[1].extends(iface))
            return SimpleVocabulary.fromItems(sorted(items, key = lambda iface: iface[0]))
    return SimpleVocabulary.fromItems([])
