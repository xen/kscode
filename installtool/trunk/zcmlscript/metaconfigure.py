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
"""ZCML Install directive handler

$Id$
"""
__author__  = "Andrey Orlov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.component.zcml import utility
from installtool.installscript.interfaces import IInstallScript
from installtool.installscript.installscript import InstallScript
from installtool import registry

class ScriptDirective(object):
    """The "install" directive handler"""

    def __init__(self, _context, factory="", name="", requires=[], script=None):
        self._context = _context
        self.factory = factory
        self.script = InstallScript(name,requires,script)
            
    def property(self,context,name="",value="") :
        self.script.context[name] = value
        
    def __call__(self) :
        registry.registerScript(self.script, self.factory) 
