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
"""SqlContainerView class for the Zope 3 based sqlcontainerview package

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.interface.declarations import classImplements
from zope.schema import getFieldsInOrder, getFieldNamesInOrder
import zope.component
from zope.publisher.browser import BrowserPage
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.app.zapi import absoluteURL
from zope.app.form.interfaces import IInputWidget, IDisplayWidget, IWidget
from zope.app.form.browser.textwidgets import TextWidget
from zope.app.form import CustomWidgetFactory
from zope.app.form.utility import setUpEditWidgets
from zope.schema._bootstrapfields import Field
from zope.component import ComponentLookupError

from simplesqlui.sqlcontainer.interfaces import ISqlContainer

class SqlContainerView(BrowserPage):
    """SQL Container View base class"""
    
    __used_for__ = ISqlContainer
    
    supportsRename = False
    supportsCut = False
    supportsCopy = False
    hasClipboardContents = False
    supportsDelete = False
    normalButtons = True
    specialButtons = False
    supportsChange = True
    
    search = []
    
    row_schema = Interface
    search_schema = Interface
    
    template = ViewPageTemplateFile("contents.pt")
    
    def __init__(self, sqlcontainer, request):
        self.context = sqlcontainer
        self.request = request
        
        self.fieldNames = getFieldNamesInOrder(self.row_schema)
        self.fields = getFieldsInOrder(self.row_schema)
        
        self.setUpSearch()
        
    def setUpSearch(self):
        if len(self.context) and self.search_schema != Interface:
            self.searchable = True
            
            attr = dict([(field, None) for field in getFieldNamesInOrder(self.search_schema)])
            searchClass = type("searchClass", (object, ), attr)
            classImplements(searchClass, self.search_schema)
            self.searchObj = searchClass()
            searchAttr = {"context" : self.searchObj, "request" : self.request}
            self.searchViewClass = type("searchViewClass", (object, ), searchAttr)
          
            self.search = []
            names = setUpEditWidgets(self.searchViewClass, self.search_schema, self.searchObj, None, False, None, self.searchObj, True, True)
            
            for fieldName in names:
                key = "field.%s" % fieldName
                name = "%s_widget" % fieldName
                widget = getattr(self.searchViewClass, name)
                widget.displayWidth = ""                
                
                self.search.append((key, widget))
        else:
            self.searchable = False
        
    def setUpWidgets(self, item):
        self.names = setUpEditWidgets(self, self.row_schema, item, None, False, None, item, True, True)
        
        return self.names
    
    def getWidget(self, item, fieldName):
        if fieldName in self.names:
            name = "%s_widget" % fieldName
            widget = getattr(self, name)
            widget.displayWidth = ""
            widget.setRenderedValue(getattr(item, fieldName))
            return widget
        else:
            return ""
        
    def __call__(self, *kv, **kw):
        """call page"""
        return self.show(*kv, **kw)
    
    def show(self, *kv, **kw):
        """show page"""
        return self.template(*kv, **kw)
    
    def checkItem(self, oddrow):
        """check item"""
        #TODO: возможно необходимо получать итератор с помощью отдельного sql скрипта
        #возможно для этого потребуется добавить метод в SqlContainer
        print "--------------------CHECKING----------------------"
        status = True
        for fieldName, widget in self.search:
            print dir(widget)
            field = widget._getFormValue()
            print "field --> ", field
            
            attrName = fieldName[len("field."):]
            attr = getattr(oddrow, attrName)
            print "attr --> ", attr
            
            try:
                if not (not field or field == attr or field in attr):
                    status = False
                    break
            except:
                status = False
                break
        
        return status
    
    def __iter__(self):
        """generator"""
        
        for name, value in self.context.items():
            if self.checkItem(value):
                yield (name, value)
    
