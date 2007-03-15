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
"""Interface of ZCML metadirective "zcml:install"

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface
from zope.component.zcml import IUtilityDirective
from zope.schema import Text
from zope.configuration.fields import GlobalObject, GlobalInterface, Tokens
from installtool.zcmlinstall.metadirectives import IPropertySubdirective
from zope.schema import Text, TextLine, Field, Bool, Datetime


class IScriptDirective(IUtilityDirective):
    """The "Script" directive interface"""
    
    script = GlobalObject(title=u"Script", required=False)    
    
    requires = Tokens(title=u"RequiredName", value_type=Text())

    name = TextLine(title=u"ScriptName")
    
    factory = TextLine(title=u"FactoryName")
    