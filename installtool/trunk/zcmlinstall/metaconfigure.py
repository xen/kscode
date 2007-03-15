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
from zope.component.interfaces import IFactory
from installtool.factory.factory import FactoryBase
from  zope.app.folder.folder import Folder
from installtool import factories

metaconfigure = factories.__dict__
class InstallDirective(object):
    """The "install" directive handler"""

    def __init__(self, _context, root=Folder, factory=None, name="", provides=IFactory, **kw):
        super(InstallDirective, self).__init__(_context, **kw)
        self.kw = kw.copy()
        self._context = _context
        self.name = name
        self.provides = provides
        self.param = {}
        if factory is not None :
            raise TypeError,"Parameter factory is forbidden in this context"
            
        self.factory = metaconfigure[str(name)] = type(str(name), (FactoryBase,), {
            'root' : root,
            '__module__' : str(factories.__name__),
            'scriptname' : name
            })
            
    def property(self,context,name="",value="") :
        self.param[name] = value
        
    def __call__(self) :
        print "INSTALL",self.factory, self.param
        print "Utility",self.provides,self.factory,self.name,self.kw
        self.factory.context = self.param.copy()        
        print "ffo1"
        print self.provides,self.factory,"%s.%s" % (str(factories.__name__),str(self.name)),self.kw
        utility(self._context, 
            provides=self.provides, 
            factory=self.factory, 
            name="%s.%s" % (str(factories.__name__),str(self.name)),
            **self.kw)
        print "ffo2"