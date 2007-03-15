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
"""ResourceView class for the Zope 3 based resourceview package

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.publisher.browser import BrowserView    
from zope.interface import implements
from contentclass2resource.interfaces import IContentClassResource, IResourceContainer
from zope.schema import getFieldNames
from zope.security.proxy import removeSecurityProxy
import zope.app.zapi

class ResourceView(BrowserView) :
    implements(IContentClassResource)
    
    def __init__(self,*kv,**kw) :
        
        super(ResourceView, self).__init__(*kv,**kw)
        
        # Получаем из контекста SiteManager
        sitemanager = zope.app.zapi.getSiteManager(self.context)

        # Получаем из SiteManager все регистрации
        utils = sitemanager.getAllUtilitiesRegisteredFor(IResourceContainer)
        if not utils:
            raise "Can't find utility for IContentClassResource!"
        
        # Получаем из контекста полное наименование объекта
        name = "%s.%s" % (removeSecurityProxy(self.context).__module__,
                          self.context.__class__.__name__)
        
        # Берём сам объект и присваиваем себе значения его полей
        obj = utils[0][name]
        for x in getFieldNames(IContentClassResource):
            setattr(self, x, getattr(obj, x))
