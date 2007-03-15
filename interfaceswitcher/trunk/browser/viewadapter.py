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
"""Mix-in adapter for interface switching view

$Id$
"""
__author__  = "Anatoly Zaretsky"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import directlyProvidedBy, alsoProvides, noLongerProvides, implementedBy, providedBy, directlyProvidedBy, directlyProvides
from zope.proxy import getProxiedObject

from interfaceswitcher.interfaceswitchervocabulary.interfaceswitchervocabulary \
    import interfaceSwitcherVocabulary


import zope.app.folder.interfaces

class ViewAdapter(object):

    def getData(self):
        obj = getProxiedObject(self.context)
        known_ifaces = interfaceSwitcherVocabulary(self.context)
        for iface in directlyProvidedBy(obj):
            if iface in known_ifaces:
                return {'marker' : known_ifaces.getTerm(iface).value}
        else:
            return {'marker' : ''}

    def setData(self, data):
        obj = getProxiedObject(self.context)
        known_ifaces = interfaceSwitcherVocabulary(self.context)
        for iface in directlyProvidedBy(obj):
            if iface in known_ifaces:
                noLongerProvides(obj, iface)
        alsoProvides(obj, data['marker'])
        return u"Saved changes."
