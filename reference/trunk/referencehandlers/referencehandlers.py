### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/) 
# Все права защищены, 2006-2007                              
#
# Developed by Key Solutions (http://keysolutions.ru/)                             
# All right reserved, 2006-2007                                       
#######################################################################                                                 #
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################

"""Interfaces for the Zope 3 based reference package

$Id$
"""
__author__  = "Anton Oprya"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from reference.referenceannotation.interfaces import IReferenceTuple
from zope.app import intid
from zope import component

def copyIReferable(ob,event):
    if event.newParent and event.newName:
        newob = IReferenceTuple(ob)
        references = newob.references
        try:
            ids=component.getUtility(intid.interfaces.IIntIds)
        except:
            return
        for ref in references:
            ids.register(ref)
            ref.parent2=ids.getId(ob)
            newrefclass = ref.__class__
            brob=ids.getObject(ref.parent1)
            rtbrob=IReferenceTuple(brob)
            rtbrob.setlink(ref)

def delIReferable(ob,event):
    delob=IReferenceTuple(ob)
    try:
        ids=component.getUtility(intid.interfaces.IIntIds, context=ob)
    except:
        return
    references=delob.references
    for ref in references:
        if ref.parent1 != ref.parent2:
            brob=ids.getObject(ref.parent1)
            rtbrob=IReferenceTuple(brob)
            rtbrob.dellink(ref)