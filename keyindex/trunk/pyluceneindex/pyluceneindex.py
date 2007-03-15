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
"""MetaIndex class for the Zope 3 based reference package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
__based_on__ = "nuxeo.lucene.catalog http://www.nuxeo.org"

from zope.interface import Interface, implements
from keyindex.keyindexbase import KeyIndexBase
from keyindex.interfaces import ID_STATE_OFF
from zope.app.container.contained import Contained
from zope.app.catalog.interfaces import ICatalogIndex
from nuxeo.lucene.catalog import LuceneCatalog, _field_id_cache, logger
from nuxeo.lucene.field import LuceneFieldConfiguration
from interfaces import IPyLuceneIndex, IPyLuceneIndexContained
from zope.index.interfaces import IStatistics
from keyxmlquery import KeyXMLQuery, KeyXMLSearchQuery
import logging
import base64
from zope.schema import Text, Datetime
import datetime
from BTrees.OOBTree import OOBTree
from nxlucene.rss.resultset import ResultSet
from nxlucene.rss.adapter import PythonResultSet
from keydate import getStringFromDateTime, \
                    getDateTimeFromString

ID_FIELD = 'uid'

TYPE2FIELDTYPE = {}

from keyindex.interfaces import _

class PyLuceneIndexBase(LuceneCatalog):
    """See IKeyIndexBase"""

    implements(IPyLuceneIndex, IStatistics)

    def __init__(self, interface=None, *args, **kwargs):
        super(PyLuceneIndexBase, self).__init__(interface, *args, **kwargs)

        self.fields = OOBTree()
        self.schema = OOBTree()

        # xmlrpc write calls after the transaction.
        self._txn_async = True

    def getFieldConfigurationsFor(self, iface=None):
        """Return tuple of field configurations in index for given interface."""
        return tuple([LuceneFieldConfiguration(key,
                                               key,
                                               type=self._getTypeByFieldType(value)
                                               )
                      for (key,value) in self.getInterfaceFields().items()])

    def _getTypeByFieldType(self, type):
        if isinstance(type,Datetime):
            return 'DATE'
        else:
            return 'TEXT'

    def _getFieldTypeById(self, id, iface=None):

        typ = _field_id_cache.get((iface,id))
        if typ is not None:
            return typ

        logger.debug('_getFieldTypeById cache miss: %s (iface=%s)', id, iface)
        for fieldconf in self.getFieldConfigurationsFor():
            if fieldconf.name == id:
                typ = fieldconf.type
                break
        else:
            typ = ''
        _field_id_cache[(iface,id)] = typ
        return typ

    def _getFieldAnalyzerById(self, id, iface=None):
        for fieldconf in self.getFieldConfigurationsFor():
            if fieldconf.name == id:
                return fieldconf.analyzer
        return ''

    def index(self, uid, ob, indexes=()):
        """Index an document. Get uid, object and tuple of field names (optional) for filtering"""
        # XXX We could filter on the interface implemented by ob in
        # the future. Right now only zope.interface.Interface is
        # considered. This is an enhacement anyway.

        field_confs = self.getFieldConfigurationsFor()
        if indexes:
            field_confs = [x for x in field_confs if x.name in indexes]

        # Build the XML query.
        xml_query = KeyXMLQuery(self.getObjectAttributes(ob), field_confs).getStream()


        # Compress the stream
        b64 = base64.b64encode(xml_query)


        # XML-RPC call
        return self._xmlrpc('indexDocument', default=False,
                            args=(uid, b64, True), async=self._txn_async)

    def reindex(self, uid, ob, indexes=()):
        """ReIndex an document. Get uid, object and tuple of field names (optional) for filtering"""
        # XXX We could filter on the interface implemented by ob in
        # the future. Right now only zope.interface.Interface is
        # considered. This is an enhacement anyway.

        field_confs = self.getFieldConfigurationsFor()
        if indexes:
            field_confs = [x for x in field_confs if x.name in indexes]

        xml_query = KeyXMLQuery(ob, field_confs).getStream()

        # Compress the stream
        b64 = base64.b64encode(xml_query)

        # XML-RPC call
        return self._xmlrpc('reindexDocument', default=False,
                            args=(uid, b64, True), async=self._txn_async)

    def unindex(self, uid):
        """UnIndex an document. Get uid of object"""
        return self._xmlrpc('unindexDocument', default=False,
                            args=(uid,), async=self._txn_async)

    def addFieldFor(self, iface=None, **kw):
        """Add field for given interface"""

    def searchResults(self, return_fields=(), search_fields=(), options=None):
        """Search for query. Get return fields list, search fields list. Return tuple of 2 elements. 1-st is list of dicts corresponding search results"""
        if not return_fields:
            return_fields = tuple(self.getFieldNamesFor())

        if options is None:
            options = {}

        # Simple case -> mapping from field_id to field_value
        search_fields_prepared = ()
        if isinstance(search_fields, dict):
            for k, v in search_fields.items():
                search_fields_prepared += ({'id' : k, 'value' : v},)
            search_fields = search_fields_prepared

        # Tuple of field confs
        fieldconfs = ()
        for field_conf in search_fields:

            # Exclude field names that are not within the fields
            # configurations. uid is a specific case here.
            if (field_conf['id'] != 'uid' and
                field_conf['id'] not in self.getFieldNamesFor()):
                logger.debug("Exclude %s from query" % field_conf['id'])
                continue

            fieldconfs += ({'id' : field_conf['id'],
                            'value' : field_conf['value'],
                            'type' : self._getFieldTypeById(field_conf['id']),
                            'condition' : field_conf.get('condition', 'AND'),
                            'analyzer' :
                            self._getFieldAnalyzerById(field_conf['id']),
                            'usage' : field_conf.get('usage', ''),
                            },)

        stream = KeyXMLSearchQuery(
            return_fields, fieldconfs, options).getStream()

        # XML-RPC sync call.
        rss = self._xmlrpc(
            'searchQuery', default='', args=(stream,), async=False)

        # Adapt the rss to a Python dictionnary
##        logger.debug("%s" %
##                     str(len(PythonResultSet(ResultSet(rss)).getResults()))[0])

        # Adapt the RSS to Python mapping.
        pyresults = PythonResultSet(ResultSet(rss)).getResults()

        results =()
        for item_map in pyresults[0]:
            converted_item_map = item_map
            for k, v in item_map.items():
                # Create datetime object.
                if self._getFieldTypeById(k).upper() == 'DATE':
                    if v:
                        converted_item_map[k] = getDateTimeFromString(v)
                    else:
                        converted_item_map[k] = v
                if self._getFieldTypeById(k).upper() == 'MULTIKEYWORD':
                    if not isinstance(v, list):
                        # Cast to a list.
                        converted_item_map[k] = [v]
            results += (converted_item_map,)
        return (results, pyresults[1])

    def index_doc(self, docid, ob):
        """Index or update document"""
        if self.state == ID_STATE_OFF:
            return
        self.index(docid, ob)

    def unindex_doc(self, docid):
        """Unindex document"""
        if self.state == ID_STATE_OFF:
            return
        self.unindex(docid)

    def apply(self, query):
        """Get search results"""
        if self.state == ID_STATE_OFF:
            return ()
        res = [int(i[ID_FIELD]) for i in self.searchResults(search_fields=query)[0]]
        return res

    def clear(self):
        """Clear index"""
        if self.state == ID_STATE_OFF:
            return
        self.clean()

    def documentCount(self):
        """Get document count"""
        if self.state == ID_STATE_OFF:
            return 0
        return self._xmlrpc('getNumberOfDocuments', default=False,
                            args=(), async=False)

    def wordCount(self):
        """Get Word Count"""
        if self.state == ID_STATE_OFF:
            return 0
        return self.documentCount()

class PyLuceneIndex(KeyIndexBase, PyLuceneIndexBase, Contained):
    implements(ICatalogIndex, IPyLuceneIndexContained)

