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

import logging
import datetime
from time import strptime

logger = logging.getLogger("keyindex.pyluceneindex.keydate")

TIME_FMT = "%Y-%m-%d %H:%M:%S"

def getDateTimeFromString(date_str):
    """Return a datetime object from date_str

    If date_str is not a valid then return the 0 UTC date.

    >>> getDateTimeFromString('2006-04-25 11:53:21')
    datetime.datetime(2006, 4, 25, 11, 53, 21)

    Buggy or missing dates:

    >>> epoch = datetime.datetime.utcfromtimestamp(0)
    >>> getDateTimeFromString('2006/04/25 11:53:21') == epoch
    True
    >>> getDateTimeFromString('') == epoch
    True
    >>> getDateTimeFromString('None') == epoch
    True
    """

    if not date_str or date_str == 'None':
        return datetime.datetime.utcfromtimestamp(0)

    try:
        return datetime.datetime(*strptime(date_str, TIME_FMT)[0:6])
    except ValueError:
#        logger.debug("getDateTimeFromString() "
#                     "Could not convert %s to datetime object " % date_str)
        return datetime.datetime.utcfromtimestamp(0)


def getStringFromDateTime(date):
    """Return a datetime object from date_str

    Take care of format since it will be reconverted in the other direction at
    the end
    """
    if date is None:
        return ''
    else:
        if date == datetime.datetime.min:
            date = datetime.datetime(1900,1,1)
        return date.strftime(TIME_FMT)
