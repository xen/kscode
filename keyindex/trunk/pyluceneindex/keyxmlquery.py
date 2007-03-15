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
"""nuxeo.lucene.xmlquery for the Zope 3 package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
__based_on__ = "nuxeo.lucene.catalog http://www.nuxeo.org"

from nuxeo.lucene.xmlquery import XMLQuery, \
                                  XMLSearchQuery, \
                                  NXLuceneElement, \
                                  logger, \
                                  stringify
from datetime import datetime
import base64
from keydate import getStringFromDateTime, \
                    getDateTimeFromString
                                                            
RANGE_QUERY_FORMAT = "[%s TO %s]"
import cElementTree as etree
import sys

class KeyXMLQuery(XMLQuery):

    def __init__(self, objectAttributes, fieldconfs=()):

        self._doc = NXLuceneElement('doc')
        fields = NXLuceneElement('fields')
        for fieldconf in fieldconfs:

            ret = objectAttributes[fieldconf.attribute]

            if isinstance(ret, datetime):
                ret = getStringFromDateTime(ret)

            field = NXLuceneElement('field')

            field.attrib['id'] = fieldconf.name
            field.attrib['attribute'] = fieldconf.attribute
            field.attrib['type'] = fieldconf.type
            field.attrib['analyzer'] = fieldconf.analyzer

            value = ''
            if isinstance(ret, (list, tuple)):
                if fieldconf.type == 'Path':
                    value = '/'.join(ret)
                else:
                    value = '#'.join(stringify(v) for v in ret)
            else:
                value = ret

            # take care of int values
            if not isinstance(value, basestring):
                value = str(value)
            else:
                try:
                    # decode from unicode, encode in utf-8
                    value = value.encode('utf-8')
                except UnicodeDecodeError:
                    # BBB
                    value = str(value)
            # Base64 encoding.
            field.text = base64.b64encode(value)

            fields.append(field)
        self._doc.append(fields)
        
class KeyXMLSearchQuery(XMLSearchQuery):

    def __init__(self, return_fields=(), fieldconfs=(), options={}):

        self._doc = NXLuceneElement('search')

        # XXX make this configurable.
        ianalyzer = NXLuceneElement('analyzer')
        ianalyzer.text = 'standard'
        self._doc.append(ianalyzer)

        # Return fields
        ireturn_fields = NXLuceneElement('return_fields')
        for return_field in return_fields:
            ifield = NXLuceneElement('field')
            ifield.text = return_field
            ireturn_fields.append(ifield)
        self._doc.append(ireturn_fields)

        # fields
        ifields = NXLuceneElement('fields')
        for fieldconf in fieldconfs:

            k = fieldconf['id']
            v = fieldconf['value']
            t = fieldconf['type']
            c = fieldconf['condition']
            a = fieldconf['analyzer']
            u = fieldconf.get('usage', '')

            ifield = NXLuceneElement('field')

            ifield.attrib['id'] = k
            ifield.attrib['type'] = t
            ifield.attrib['condition'] = c
            ifield.attrib['analyzer'] = a
            ifield.attrib['usage'] = u

            if k + '_usage' in options.keys():
                # Get usage ZCatalog way for range query.
                # We strictly don't care about the ZCatalog
                # deprecation since it's quite handly in here.
                u = options.get(k+'_usage')
                ifield.attrib['usage'] = u

            # XXX change this. Hardcoded for now. Use a tokenizer
            # server side.
            if isinstance(v, str) or isinstance(v, unicode):
                ifield.attrib['value'] = v
            elif isinstance(v, list) or isinstance(v, tuple):
                if len(v) == 2:
                    if v[0] is None and v[1] is None:
                        continue
                    elif isinstance(v[0], datetime) \
                         or isinstance(v[1], datetime):
                        if v[0] is None:
                            v = (datetime.min, v[1])
                        elif v[1] is None:
                            v = (v[0], datetime.max)
                        v = tuple([getStringFromDateTime(i) for i in v])
                ifield.attrib['value'] = '#'.join(v)
            else:
                ifield.attrib['value'] = str(v)
            ifields.append(ifield)

        self._doc.append(ifields)

        # Batching start
        elt = NXLuceneElement('batch')

        b_start = options.get('b_start', 0)
        b_size  = options.get('b_size', sys.maxint)

        elt.attrib['start'] = str(b_start)
        elt.attrib['size'] = str(b_size)
            
        self._doc.append(elt)

        # Operator
        op = options.get('operator')
        if op is not None:
            elt = NXLuceneElement('operator')
            elt.text = op
            self._doc.append(elt)

        # Sort
        elt = NXLuceneElement('sort')

        sort_on = options.get('sort-on')
        if sort_on is not None:
            subelt = NXLuceneElement('sort-on')
            subelt.text = sort_on
            elt.append(subelt)

        sort_limit = options.get('sort-limit')
        if sort_limit is not None:
            subelt = NXLuceneElement('sort-limit')
            subelt.text = str(sort_limit)
            elt.append(subelt)

        sort_order= options.get('sort-order')
        if sort_order is not None:
            subelt = NXLuceneElement('sort-order')
            subelt.text = str(sort_order)
            elt.append(subelt)

        self._doc.append(elt)

    def getStream(self):
        return etree.tostring(self._doc, encoding="UTF-8")