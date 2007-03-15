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
"""RuntimeErrorView class for the Zope 3 based factory package

$Id$
"""
__author__  = "Sergey Shilov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"
 
from zope.publisher.browser import BrowserView
                
class RuntimeErrorView(BrowserView):
    """Вид для отображения ошибки времени выполнения"""
    def getScripts(self):
        """Возвращает список наименований успешно выполненных скриптов"""

        print "--------------- getScripts --------------------------------"
        print dir(self)
        print "QQQ:"
        return [item[0] for item in self.context.res]
