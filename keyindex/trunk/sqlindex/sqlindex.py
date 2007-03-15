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
"""SQLIndex class for the Zope 3 based index package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface, implements
from keyindex.keyindexbase import KeyIndexBase
from zope.app.container.btree import BTreeContainer
from zope.app.catalog.interfaces import ICatalogIndex
from zope.index.interfaces import IStatistics, IInjection, IIndexSearch
from interfaces import ISQLIndex, ISQLIndexContainer
from keyindex.interfaces import ID_STATE_OFF

from keyindex.interfaces import _

SELECT = 'select'
INSERT = 'insert'
DELETE = 'delete'
DELETE_ALL = 'delete_all'
UPDATE = 'update'
EXISTS = 'exists'
DOCUMENT_COUNT = 'document_count'
WORD_COUNT = 'word_count'

ID_FIELD = 'Id'

MIN_FORMAT = '%s_min'
MAX_FORMAT = '%s_max'

class SQLIndexBase(object):
    """See IKeyIndexBase"""

    implements(ISQLIndex)

    connectionName = None

    def escape(s):
        return s

    def select(self, args):
        """Insert row"""
        script = self.get(SELECT, None)
        if script is not None:
            print "ARGS:",args
            res = script(**args)
            return res

    def exists(self, docid):
        script = self.get(EXISTS, None)
        if script is not None:
            args = {ID_FIELD: docid}
            res = script(**args)
            if res:
                return True
        return False

    def insert(self, docid, args):
        """Insert row"""
        script = self.get(INSERT, None)
        if script is not None:
            args[ID_FIELD] = docid
            #print '-------------------insert-------------------------'
            #print args
            res = script(**args)
            return res

    def update(self, docid, args):
        """Insert row"""
        script = self.get(UPDATE, None)
        if script is not None:
            args[ID_FIELD] = docid
            res = script(**args)
            return res

    def delete(self, docid):
        """Delete row"""
        script = self.get(DELETE, None)
        if script is not None:
            args = {ID_FIELD: docid}
            res = script(**args)
            return res

    def delete_all(self):
        """Delete all records"""
        script = self.get(DELETE_ALL, None)
        if script is not None:
            args = {}
            res = script(**args)
            return res

    def index_doc(self, docid, ob):
        """Index or update document"""
        if self.state == ID_STATE_OFF:
            return
        if object is not None:
            vals = self.getObjectAttributes(ob)
            print '----------------vals----------------'
            print vals
            if self.exists(docid):
                self.update(docid, vals)
            else:
                self.insert(docid, vals)

    def unindex_doc(self, docid):
        """Unindex document"""
        if self.state == ID_STATE_OFF:
            return 0
        self.delete(docid)

    def apply(self, query):
        """Get search results"""
        if self.state == ID_STATE_OFF:
            return ()
        res = self.select(query)
        res = [int(getattr(i, ID_FIELD.lower())) for i in res]
        return res

    def clear(self):
        """Clear index"""
        if self.state == ID_STATE_OFF:
            return
        self.delete_all()

class SQLIndexStatBase(object) :
    implements(IStatistics)

    def document_count(self):
        """Get Document Count"""
        script = self.get(DOCUMENT_COUNT, None)
        if script is not None:
            args = {}
            res = script(**args)
            return getattr(res[0], DOCUMENT_COUNT, 0)
        return 0

    def word_count(self):
        """Get Word Count"""
        script = self.get(WORD_COUNT, None)
        if script is not None:
            args = {}
            res = script(**args)
            return getattr(res[0], WORD_COUNT, 0)
        return 0

    def documentCount(self):
        """Get document count"""
        if self.state == ID_STATE_OFF:
            return 0
        return self.document_count()

    def wordCount(self):
        """Get Word Count"""
        if self.state == ID_STATE_OFF:
            return 0
        return self.word_count()


class SQLIndex(KeyIndexBase, SQLIndexBase, SQLIndexStatBase, BTreeContainer):
    implements( ISQLIndexContainer, ICatalogIndex)
