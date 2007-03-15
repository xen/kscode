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
"""ZCML factoryform directive handler

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.component.zcml import utility
from zope.component.interfaces import IFactory
from installtool.factory.factory import FactoryBase
from  zope.app.folder.folder import Folder
from installtool import factories
from installtool.zcmlinstall.metaconfigure import InstallDirective
from zope.app.component.contentdirective import ClassDirective
from zope.app.form.browser.metaconfigure import AddFormDirective
from zope.schema import getFieldNames
from zope.app.publisher.browser.menumeta import addMenuItem
from add import AddMixIn

metaconfigure = factories.__dict__

class FactoryFormDirective(InstallDirective):
    """The "factoryform" directive handler"""

    def __init__(self, _context, root=Folder, factory=None, name="",
                 provides=None, class_=None, 
                 schema=None, for_=None, permission=None, view='', title='',
                 description='', **kw):

        super(FactoryFormDirective, self).__init__(_context, root=root,
             name=name, provides=IFactory, **kw)

        if factory is not None :
            raise ValueError,"factory must be None in this context"            
            
        if provides is not None :
            raise ValueError,"provides must be None in this context"            

        self.schema = schema
        self.for_ = for_
        self.permission = permission
        self.view = view
        self.title = title
        self.description = description

        if class_:
            self.class_ = type(class_, AddMixIn, {})
        else:
            self.class_ = AddMixIn

    def __call__(self) :
        super(FactoryFormDirective, self).__call__()

        obj = ClassDirective(self._context, self.factory)
        obj.require(self._context, permission=self.permission, interface=[IFactory,])
        obj()

        AddFormDirective(self._context, name=self.view,
            content_factory_id=str("installtool.factories.%s" % self.name), schema=self.schema,
            class_=self.class_, permission=self.permission,
            keyword_arguments=getFieldNames(self.schema), for_=self.for_)()
        
        addMenuItem(self._context, 
            title = self.title, description=self.description,
            factory=str("installtool.factories.%s" % self.name), 
            view=self.view, 
            permission=self.permission)
