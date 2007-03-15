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
"""Interfaces for the Zope 3 based metaindex package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from zope.interface import Interface
from zope.app.container.interfaces import IContained
from zope.schema import Field, TextLine
from zope.app.container.constraints import ContainerTypesConstraint
from zope.app.catalog.interfaces import ICatalog
from nuxeo.lucene.interfaces import ILuceneCatalog
from keyindex.interfaces import IKeyIndex

from keyindex.interfaces import _

class IPyLuceneIndex(ILuceneCatalog, IKeyIndex) :
    """ Список параметров,позволяющих подключится к PyLucene """

    server_url = TextLine(
        title=_(u"Server URL"),
        description=_(u"XML-RPC server URL"),
        required=True,
        default=u'http://localhost:9180',
        )

class IPyLuceneIndexContained(IContained) :
    """PyLucene index contained"""

    __parent__ = Field(
    constraint = ContainerTypesConstraint(ICatalog))


