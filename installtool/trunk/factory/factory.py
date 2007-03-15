### -*- coding: utf-8 -*- #############################################
# Разработано компанией Ключевые Решения (http://keysolutions.ru/) 
# Все права защищены, 2006-2007
#
# Developed by Key Solutions (http://keysolutions.ru/)
# All right reserved, 2006-2007
######################################################################
# Licensed under the Zope Public License, Version 2.1 (the "License"); you
# may not use this file except in compliance with the License. A copy of the
# License should accompany this distribution.
#
# This software distributed under the License is distributed on an "AS IS"
# BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
#######################################################################
"""Factory class for the Zope 3 based installtool package

$Id$
"""
__author__  = "Andrey Orlov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__    = "$Date$"
 
from zope.interface import Interface
from zope.app.zapi import getSiteManager 
from topolsort import topSort, SortIsNotPossible, UnknownDependency
from zope.interface import implements,implementedBy
from zope.component.interfaces import IFactory
from installtool.installerregistry.interfaces import IInstallerRegistry
from installtool.exceptions import ScriptError, UnresolvedDepsError, UnknownDependencyError

class FactoryBase(object) :
    implements(IFactory)
    
    root = lambda x : None
    scriptname = ""
    context = {}

    def __call__(self,*kv,**kw) :
        print "CALL",kv,kw
        self.ob = self.root()
        self.context.update(kw)
        #self.runScripts()
        return self.ob
                        
    def getInterfaces(self,*kv,**kw) :
        return implementedBy(self.root)

    def getScripts(self):
        """Return script records, registered for factory """

        return topSort(
            [ob \
                for ob in \
                    getSiteManager().getUtility(IInstallerRegistry) \
                        .queryScript(self.scriptname) \
                ]
        )

    def runScripts(self,ob):
        """Run scripts in factory context """ 
        print "Context:", ob,self.context        
        res = []
        try:
            for script in self.getScripts() :
                try:
                    res.append((script.name,script(self.ob,self.context)))
                except Exception,msg:
                    print "There are some errror during run script:",msg
                    raise ScriptError(script.name,msg,res)
        except SortIsNotPossible, details:
            print "Can't resolve dependencies!"
            raise UnresolvedDepsError(details)
        except UnknownDependency, details:
            print details[0]
            raise UnknownDependencyError(details[0])
        return res
