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
"""SqlVocabulary views

$Id$
"""
__author__  = "Anton Oprya"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import implements
from sqlvocabulary.interfaces import ISqlScriptGenerate, ISqlVocabulary  
from zope import schema
from zope.rdb.interfaces import DatabaseException

class SqlScriptGenerate(object):
    """Views for product sqlvocabulary.
    """
    
    sqlscript_template = "select %s, %s from %s"
        
    def getData(self,*kv,**kw) :
        return [ (x,getattr(self.context,x)) for x in 
                schema.getFieldNames(ISqlScriptGenerate)]

    def setData(self,d,**kw) :
        for x in schema.getFieldNames(ISqlScriptGenerate) :
            setattr(self.context,x,d[x])
        
        self.context.source = self.sqlscript_template % (self.context.call, self.context.id,
                                                         self.context.table)
        if self.context.condition:
            self.context.source += ' where ' + self.context.condition
        return 'SQL Script (' + self.context.source + ') Generated'


class SQLScriptTest(object):
    """Test the SQL inside the SQL Script
    """

    __used_for__ = ISqlVocabulary

    error = None

    def getArguments(self):
        form = self.request.form
        arguments = {}

        for argname, argvalue in self.context.getArguments().items():
            value = form.get(argname)
            if value is None:
                value = argvalue.get('default')
            if value is not None:
                arguments[argname.encode('UTF-8')] = value
        return arguments

    def getTestResults(self):
        try:
            return self.context.__call2__(**self.getArguments())
        except (DatabaseException, AttributeError, Exception), error:
            self.error = error
            return []

    def getFormattedError(self):
        error = str(self.error)
        return error

    def getRenderedSQL(self):
        return self.context.getTemplate()(**self.getArguments())