### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/) 
# Все права защищены, 2006-2007
#
# Developed by Key Solutions (http://keysolutions.ru/)
# All right reserved, 2006-2007
######################################################################
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################
"""Exception classes for the Zope 3 based installtool package

$Id$
"""
__author__  = "Andrey Orlov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__    = "$Date$"

from zope.interface import implements
from interfaces import IScriptError, IUnresolvedDepsError, IUnknownDependencyError

class ScriptError(Exception) :
    implements(IScriptError)

    def __init__(self,script,msg,res) :
        Exception.__init__(self,script,msg,res)
        self.script = script
        self.msg = msg
        self.res = res

class UnresolvedDepsError(Exception) :
    implements(IUnresolvedDepsError)

    def __init__(self, res) :
        Exception.__init__(self, res)
        self.res = res

class UnknownDependencyError(Exception) :
    implements(IUnknownDependencyError)

    def __init__(self, msg) :
        #Exception.__init__(self, msg,res)
        Exception.__init__(self, msg)
        self.msg = msg

