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
"""Interfaces for the Zope 3 based factory package

$Id$
"""
__author__  = "Arvid"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface

from zope import schema 
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import ItemTypePrecondition
from zope.app.container.constraints import ContainerTypesConstraint
                
class ISqlFactory(Interface):
    """factory interface"""
    
    def generate(data, parent):
        """generate object which have parent record"""
    

class ISqlFactoryProp(Interface):
    """Factory properties interface"""
    
    datasource = schema.Choice(
                            title = u"Data source name"
                            ,description = u"The Data source name for the database access to be used."
                            ,vocabulary = "DS Vocabulary"
                            ,required = True
                            )
    
    ids = schema.Tuple(
                            title = u"Identifiers"
                            ,description = u"Identifiers"
                            ,value_type=schema.TextLine(title = u"Identifier")
                            )
    
    #TODO: тут явно что-то не так
    factory = schema.Choice(
                            title = u"Record factory"
                            ,description = u"Record factory"
                            ,vocabulary = "Record Base Vocabulary"
                            ,required = True
                            )
    
