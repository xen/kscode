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
"""Interfaces for the Zope 3 based metaindex package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.app.container.interfaces import IContainer
from zope.app.container.constraints import ItemTypePrecondition
from zope.schema import TextLine, Choice
from zope.app.sqlscript.interfaces import ISQLScript
from keyindex.interfaces import IKeyIndex

from keyindex.interfaces import _

class ISQLIndex(IKeyIndex) :
    """ Список параметров,позволяющих подключится к SQL"""

    connectionName = Choice(
        title=_(u"Connection Name"),
        description=_(u"The Connection Name for the connection to be used."),
        vocabulary="Connection Names",
        required=False)

class ISQLIndexContainer(IContainer) :
    """SQL method container"""

    def __setitem__(self, name, value):
        pass

    __setitem__.precondition = ItemTypePrecondition(ISQLScript)


