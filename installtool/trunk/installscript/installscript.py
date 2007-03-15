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
"""InsltallScript class for the Zope 3 based installtool package

$Id$
"""
__author__  = ""
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface
from zope.interface import implements,implementedBy
from installtool.installscript.interfaces import IInstallScript
                
class InstallScript(object) :
    implements(IInstallScript)

    name = ""
    requires = []
    script = None
    context = {}
        
    def __init__(self, name, requires, script) :
        self.name = name
        self.requires = requires
        self.script = script
        self.context = {}
            
    def __call__(self, context, properties) :
        return self.script(context,**dict(((str(x),y) for x,y in properties.items())) )

