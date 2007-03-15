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
"""KeyIndexBase class for the Zope 3 based index package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import implements, \
                           Interface

from interfaces import IKeyIndex, ID_STATE_ON, ID_STATE_OFF
from zope.schema import getFields

from interfaces import _

class KeyIndexBase(object) :
    """See IBaseIndex"""

    implements(IKeyIndex)
    default_interface = None

    interface = None

    state = ID_STATE_ON

    def __init__(self, interface=None, *args, **kwargs):
        super(KeyIndexBase, self).__init__(*args, **kwargs)
        if interface is None:
            self.interface = self.default_interface
        else:
            self.interface = interface

    def index_doc(self, docid, ob):
        if self.interface is not None:
            print "INDEX:", docid, ob, self.interface
            ob = self.interface(ob, None)
            if ob is None:
                return None
            return super(KeyIndexBase, self).index_doc(docid, ob)

    def getObjectAttributes(self, ob):
        """Get object attribute values by our interface"""
        fields = getFields(self.interface)
        res = dict(#filter(lambda x: x[1] is not None, \
                          [(key, getattr(ob, key, value.default)) for (key, value) in fields.items()] \
                    #      ) \
                  )
        return res

    def getInterfaceFields(self):
        return getFields(self.interface)




