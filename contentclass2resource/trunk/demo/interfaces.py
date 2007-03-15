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
"""Interfaces for the Zope 3 based demo package

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.app.container.contained import IContained
from zope.schema import Choice

class IMyContentClass(Interface):
    pass

class IDemoResource(Interface):
    call = Choice(
        title=u'Russian name',
        description=u'Russian class name',
        vocabulary='rescon_call',
        required=True)
    icon = Choice(
        title=u'Class icon',
        description=u'Name of class icon',
        vocabulary='rescon_icon',
        required=True)
    def getData():
        pass
    def setData(data):
        pass
