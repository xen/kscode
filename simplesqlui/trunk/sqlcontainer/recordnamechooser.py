### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/)    
# Все права защищены, 2006-2007                                       
#
# Developed by Key Solutions (http://keysolutions.ru/)                
# All right reserved, 2006-2007                                       
#######################################################################
# $Id$
#######################################################################
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################
"""The NameChooser for copies Record.

$Id$
"""
__author__  = "Andrey Orlov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
__based__ = "Sergey Shilov"

from zope.interface import implements
from zope.app.container.contained import NameChooser
from zope.app.container.interfaces import INameChooser

class RecordNameChooser(NameChooser):
    """The NameChooser for IRecordObjectContent items"""
    implements(INameChooser)

    def chooseName(self, name, object):
        return self.context.add(object)    
