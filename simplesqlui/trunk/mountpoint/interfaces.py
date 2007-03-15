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
"""Interfaces for the Zope 3 based mountpoint package

$Id$
"""
__author__  = ""
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.interface import Interface

from zope import schema
from zope.app.container.interfaces import IContained, IContainer
from zope.app.container.constraints import ItemTypePrecondition
from zope.app.container.constraints import ContainerTypesConstraint

from simplesqlui.record.interfaces import IRecordContained
from interfaceswitcher.interfaces import IInterfaceSwitcherAble
                
class IMountpointProp(Interface):
    """Mountpoint properties class interface"""
    
    datasource = schema.Choice(
                            title = u"Data source name"
                            ,description = u"The Data source name for the database access to be used."
                            ,vocabulary = "DS Vocabulary"
                            ,required = True
                            )
    
    factory = schema.Choice(
                            title = u"SQL Factory"
                            ,description = u"SQL Factory"
                            ,vocabulary = "SQL Factory Vocabulary"
                            ,required = True
                            )

    dict_ = schema.Tuple(
            title = u"Initial values",
            value_type=schema.TextLine()
        )

class IMountpoint(IMountpointProp):
    """Mountpoint class interface"""
    
    ds = schema.Field()
    rf = schema.Field()
    ids = schema.Field()

##class IRecordContained(IContained):
##    pass

class IMountpointContainer(IContainer):
    """Mountpoint container class interface"""
    
    def __setitem__(name, object):
        """Add a object."""

    __setitem__.precondition = ItemTypePrecondition(IRecordContained)
    
##IRecordContained.__parent__ = schema.Field(
##            constraint = ContainerTypesConstraint(IMountpointContainer)
##            )

class IMountPointSwitcher(IInterfaceSwitcherAble):
    """Interface switcher base interface"""
    pass

