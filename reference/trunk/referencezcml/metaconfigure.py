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
"""ZCML Reference directive handler

$Id$
"""
__author__  = "Anton Oprya"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

from persistent import Persistent
from reference.reference.referencebase import ReferenceBase
from zope.app.component.contentdirective import ClassDirective
from reference import reference
metaconfigure = vars()
class AddReferenceDirective(object):
    """Reference directive handler"""
    
    def __init__(self,_context, 
        interface1=None, 
        interface2=None, 
        name="", 
        title1="",
        title2=None,
        iscommutative=False,
        isreflexive=False,
        ismultiplicative=False
        ):
        
        class_ = metaconfigure[name] = type(str(name), (ReferenceBase, Persistent), {
            '__parent1_interface__' : interface1,
            '__parent2_interface__' : interface2,
            'reference_type' : name,
            '__name__' : name,
            'title1' : title1,
            'title2' : title2 or title1,
            'iscommutative' : iscommutative,
            'isreflexive' : isreflexive,
            'ismultiplicative' : ismultiplicative,  
            })

        self.cd = ClassDirective(_context, class_= class_)
        self.cd.factory(_context,id="reference.reference.%s" % name)
        
    def __call__(self) :
        return self.cd()