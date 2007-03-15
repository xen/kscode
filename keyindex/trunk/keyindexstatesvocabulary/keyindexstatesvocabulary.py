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

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.interface import implements
from zope.schema.interfaces import IVocabularyTokenized
from keyindex.interfaces import KEYINDEX_STATES

from keyindex.interfaces import _

class KeyIndexStatesVocabulary(object):
    """IKeyIndex states vocabulary"""

    implements(IVocabularyTokenized)

    def __init__(self, context):

        self.by_value = dict( [ (z.value,z)  for z in  [ SimpleTerm(id, title=ob) for (id, ob) in KEYINDEX_STATES.items()]] )
        self.by_token = dict( [ (z.token,z)  for z in  [ SimpleTerm(id, title=ob) for (id, ob) in KEYINDEX_STATES.items()]] )

    def __contains__(self, value):
        return value in self.by_value

    def getTerm(self, value):
        return self.by_value[value]

    def getTermByToken(self, token):
        return self.by_token[token]

    def __iter__(self):
        return iter(self.by_value.values())

    def __len__(self):
        return len(self.by_value)
