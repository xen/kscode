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
"""Utility of content names vocabulary.

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.app.zapi import getUtilitiesFor
from zope.component.interfaces import IFactory
from zope.schema.vocabulary import SimpleVocabulary

def ContentNamesVocabulary(context):
    """Utility of content names vocabulary"""
    # Строим список всех классов, для которых есть фабрики (с фильтрацией
    # дубликатов и сортировкой)
    temp = {}
    for key, value in getUtilitiesFor(IFactory):
        try:
            name = '%s.%s' % (value._callable.__module__, value._callable.__name__)
            temp[name] = '!'
        except:
            pass
    return SimpleVocabulary.fromValues(sorted(temp.keys()))
