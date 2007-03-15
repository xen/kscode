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
"""ZCML sqlcontents directive handler

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.app.publisher.browser.viewmeta import page
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.schema import getFieldsInOrder

from sqlcontainerview import SqlContainerView
 
def sqlContents(_context, permission, for_, 
                            row_schema, search_schema = None,
                            name = "contents.html",
                            layer = IDefaultBrowserLayer,  
                            class_ = SqlContainerView, 
                            allowed_interface = None, allowed_attributes = None, 
                            template = None,
                            attribute = '__call__', 
                            menu = None, title = "Contents"
                            ):
    """ Set up sql container view """
    
    if for_ is None:
        raise ValueError("A interface must be specified")
    
    for fieldName, field in getFieldsInOrder(search_schema):
        if field.readonly:
            raise ValueError("Search interface can't contain readonly fields")
    
    if permission is not None:
        attr = {}
        if template:
            attr["template"] = template
        if search_schema:
            attr["search_schema"] = search_schema
        attr["row_schema"] = row_schema
        
        newClass = type("SqlContainerViewDesc", (class_, ), attr)
        
        page(_context = _context, name = name, 
                permission = permission, for_ = for_, 
                layer = layer, template = template, 
                class_ = newClass, 
                allowed_interface = allowed_interface, 
                allowed_attributes = allowed_attributes, 
                attribute = attribute, 
                menu = menu, title = title
                )
        
        page(_context = _context, name = "show", 
                permission = permission, for_ = for_, 
                layer = layer, template = None, 
                class_ = newClass, 
                allowed_interface = allowed_interface, 
                allowed_attributes = allowed_attributes, 
                attribute = "show"
                )
