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

"""SqlVocabulary classes for the Zope 3 based sqlvocabulary package

$Id$
"""
__author__  = "Anton Oprya"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.app.sqlscript import SQLScript
from zope.interface import implements, classProvides
from interfaces import ISqlVocabulary, ISqlScriptGenerate
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabulary
from zope.app.cache.caching import getCacheForObject, getLocationForCache
from zope.rdb import queryForResults

class SqlVocabulary(SQLScript, SimpleVocabulary):
    """Vocabulary, loading the content from a sql-base.
    """
    implements(ISqlVocabulary, IVocabulary,
               IVocabularyFactory, ISqlScriptGenerate)

    _terms=[]

    by_value={}

    by_token={}

    table = u''

    id = u''

    call = u''

    condition = u''

    def __call2__(self, **kw):
        arg_values = {}
        missing = []
        for name in self._arguments.keys():
            name = name.encode('UTF-8')
            try:
                arg_values[name] = kw[name]
            except KeyError:
                arg = self._arguments[name]
                try:
                    arg_values[name] = arg['default']
                except KeyError:
                    try:
                        if not arg['optional']:
                            missing.append(name)
                    except KeyError:
                        missing.append(name)

        try:
            connection = self.getConnection()
        except KeyError:
            raise AttributeError("The database connection '%s' cannot be "
                                 "found." % (self.connectionName))

        query = apply(self.template, (), arg_values)
        cache = getCacheForObject(self)
        location = getLocationForCache(self)
        if cache and location:
            _marker = object()
            result = cache.query(location, {'query': query}, default=_marker)
            if result is not _marker:
                return result
        result = queryForResults(connection, query)
        if cache and location:
            cache.set(result, location, {'query': query})
        return result

    def __call__(self, context):
        return self

    def getTermsFromSQL(self):
        self._terms=[]
        self.by_value={}
        self.by_token={}
        queryresult=self.__call2__()
        for row in queryresult:
            value = getattr(row, queryresult.columns[1])
            title = getattr(row, queryresult.columns[0])
            token = title.__repr__()
            term = SimpleTerm(value=value,token=token, title=title)
            self._terms.append(term)
            self.by_value[value] = term
            self.by_token[token] = term

    def __iter__(self):
        self.getTermsFromSQL()
        return iter(self._terms)

    def getTerm(self, value):
        self.getTermsFromSQL()
        try:
            return self.by_value[value]
        except KeyError:
            raise LookupError(value)

    def __len__(self):
        self.getTermsFromSQL()
        return len(self.by_value)

    def __contains__(self, value):
        self.getTermsFromSQL()
        try:
            return value in self.by_value
        except TypeError:
            return False


"""class SqlVocabularyFactory(SQLScriptFactory):

    def createScript(self):
        return SqlVocabulary()"""

