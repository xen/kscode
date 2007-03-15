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
"""Interface of ZCML metadirective "sqlcontents"

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope import schema
from zope.app.publisher.browser.metadirectives import IPageDirective
from zope.configuration.fields import GlobalObject, GlobalInterface 
from zope.security.zcml import Permission
 
from zope.interface import Interface
                
class ISqlContents(IPageDirective):
    """Define several container views for an 'ISqlCotainer' implementation."""
    
    name = schema.TextLine(
                    title = u"The name of the page"
                    ,description = u""
                    ,required = False
                    )
    
    row_schema = GlobalInterface(
                    title = u"The interface of content"
                    ,description = u"The interface of content"
                    ,required = False
                    ,default = Interface
                    )
    search_schema = GlobalInterface(
                    title = u"The interface of searching"
                    ,description = u"The interface of searching"
                    ,required = False
                    ,default = Interface
                    )
                    
    
