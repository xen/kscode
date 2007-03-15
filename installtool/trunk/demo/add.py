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
"""AddMixIn class for the Zope 3 based installtool package

$Id$
"""
__author__  = ""
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface
from zope.interface import implements,implementedBy
from installtool.installscript.interfaces import IInstallScript
                
class AddMixIn(object) :

    def create(self,*args, **kw):
        print "MyCreate!!"
        self._my_factory = self._factory
        print self._my_factory
        return self._my_factory(self,*args, **kw)

    def add(self, content):
        print "MyAdd!!!"
        content = super(AddMixIn,self).add(content)
        print "RunScripts!!!"
        self._my_factory.runScripts(content) 
        print "Ready!!"
        return content
