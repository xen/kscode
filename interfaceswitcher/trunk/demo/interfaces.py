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
"""Demo switchable markers

$Id$
"""
__author__  = "Anatoly Zaretsky"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from interfaceswitcher.interfaces import IInterfaceSwitcherAble


class FolderGroup(IInterfaceSwitcherAble):
    pass

class CatalogGroup(IInterfaceSwitcherAble):
    pass

class FolderOne(FolderGroup):
    pass

class FolderTwo(FolderGroup):
    pass

class CatalogOne(CatalogGroup):
    pass

class CatalogTwo(CatalogGroup):
    pass
