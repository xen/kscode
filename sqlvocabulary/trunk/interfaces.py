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
"""Interfaces for the Zope 3 based sqlvocabulary package

$Id$
"""
__author__  = "Anton Oprya"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 

from zope.app.container.interfaces import IContainer
from zope.app.sqlscript.interfaces import ISQLScript
from zope.interface import Interface
from zope.schema import TextLine


class ISqlVocabulary(Interface):
    """Vocabulary, loading the content from a sql-base.
    """
    
    def getTermsFromSQL():
        """Fills terms for Vocabulary by using SQLscript.
        """
    def __call2__():
        pass

class ISqlScriptGenerate(Interface):
    """
    """
    
    table = TextLine(title = u'Table',
                          description = u'Table',
                          default = u'',
                          required = True,)
    
    id = TextLine(title = u'Identifier',
                          description = u'Identifier',
                          default = u'',
                          required = True,)
    
    call = TextLine(title = u'Name',
                          description = u'Name',
                          default = u'',
                          required = True,)
    
    condition = TextLine(title = u'Condition',
                          description = u'Condition',
                          default = u'',
                          required = False,)
    