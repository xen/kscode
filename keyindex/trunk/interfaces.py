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
"""Interfaces for the Zope 3 based keyindex package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.schema import Choice
from zope.index.interfaces import IInjection

import zope.i18nmessageid
_ = zope.i18nmessageid.MessageFactory('keyindex')

ID_STATE_ON = True
STATE_ON = _(u'On')
ID_STATE_OFF = False
STATE_OFF = _(u'Off')

KEYINDEX_STATES = {ID_STATE_ON: STATE_ON,
                   ID_STATE_OFF: STATE_OFF}

class IKeyIndex(Interface):
    """I index objects by first adapting them to an interface"""

    interface = Choice(
        title=_(u"Interface"),
        description=_(u"Objects will be adapted to this interface"),
        vocabulary="Interfaces",
        required=False,
        )

    state =  Choice(
        title=_(u"State"),
        description=_(u"State of index (${On} or ${Off})", mapping={'On': STATE_ON,
                                                                    'Off': STATE_OFF}),
        vocabulary="KeyIndexStates",
        required=True,
        default=ID_STATE_ON
        )

#    def getObjectAttributes(object):
#        """Get Object attribute values"""
