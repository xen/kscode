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
"""Interface of ZCML metadirective "browser:factoryform"

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface
from zope.component.zcml import IUtilityDirective
from zope.schema import TextLine, Text, Id, Int, Bool
from zope.configuration.fields import GlobalObject, GlobalInterface, MessageID
from zope.security.zcml import Permission
from installtool.zcmlinstall.metadirectives import IInstallDirective

class IFactoryFormDirective(IInstallDirective):
    """The "factoryform" directive interface"""
    schema = GlobalInterface(
        title=u"Schema",
        description=u"The schema from which the form is generated.",
        required=True
        )
    
    for_ = GlobalInterface(
        title=u"Interface",
        required=False
        )
    
    permission = Permission(
        title=u"Permission",
        description=u"The permission needed to use the view.",
        required=True
        )
    
    class_ = GlobalObject(
        title=u"Addform class",
        required=False
        )
    
    view = TextLine(
        title=u"Custom view name",
        description=u"The name of a custom add view",
        required = False,
        )
    
    title = MessageID(
        title=u"Title",
        description=u"The text to be displayed for the menu item",
        required=True
        )
    
    description = MessageID(
        title=u"A longer explanation of the menu item",
        description=u"""
        A UI may display this with the item or display it when the
        user requests more assistance.""",
        required=False
        )

    

