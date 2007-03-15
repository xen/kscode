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
"""Search Engine Comparison package

$Id$
"""
__author__  = "Anatoly Bubenkov"
__license__	= "ZPL"
__version__ = "$Revision$"
__date__ = "$Date$"

import urllib2, urllib
import os
import base64
from zope.testbrowser.browser import Browser

_debug = 0

_host = None
_username = None
_password = None
_addformurl = None
_storagedir = None

_browser = None

USAGE = """Usage:
python searchenginecomparison.py -o host -u username -p password -a addformurl -s storagedir"""

TITLE_FIELD = 'field.Title'
BODY_FIELD = 'field.Body'
ANNOTATION_FIELD = 'field.Annotation'
REGION_FIELD = 'field.Region'
UPDATE_SUBMIT = 'UPDATE_SUBMIT'
PUBLISHDATETIME = 'field.PublishDateTime'
ENDPUBLISHDATETIME = 'field.EndPublishDateTime'
DATETIME = "2007-02-08 13:07:39.535517"
ENDDATETIME = "2017-02-08 13:07:39.535517"
ADDINPUTNAME = "add_input_name"
REGION = "CHRISTMAS ISLAND                                                                                                                                      "
AUTHORS_COUNT = "field.Authors.count"

REALM = '"Zope"'

class NewsUploader(object):

    def __init__(self, host, addFormUrl, storageDir):
        self.addFormUrl = urllib2.os.path.join(host, addFormUrl)
        self.storageDir = storageDir
        self.upload()

    def upload(self):
        lst = os.listdir(self.storageDir)
        print "found %s files" % len(lst)
        print 'upload started'
        for i in lst:
            path = os.path.join(self.storageDir, i)
            body = open(path, 'r')
            try:
                buf = body.read()
                buf = "".join([k for k in buf if ord(k) <= 127])
                self.upload_file(i, buf)
            finally:
                body.close()
        print 'upload finished'

    def upload_file(self, title, body):
        data={TITLE_FIELD: title,
              BODY_FIELD: body,
              ANNOTATION_FIELD: title,
              UPDATE_SUBMIT: UPDATE_SUBMIT,
              REGION_FIELD: REGION,
              PUBLISHDATETIME: DATETIME,
              ENDPUBLISHDATETIME: ENDDATETIME,
              ADDINPUTNAME:'',
              AUTHORS_COUNT:'0'}
        data = urllib.urlencode(data)
        auth = ('%s:%s' % (_username, _password)).encode('base64')
        request = urllib2.Request(self.addFormUrl, data)
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Accept-Language', 'en-US')
        res = urllib2.urlopen(request)
        print res.read()

class CatalogReindexer(object):

    def __init__(self, host, catalogReindexUrls):
        self.catalogUrls = [urllib2.os.path.join(host, i) for i in catalogReindexUrls]
        self.reindex()

    def reindex(self):
        print "found %s catalogs" % len(self.catalogUrls)
        print 'reindex started'
        for i in self.catalogUrls:
            self.reindex_catalog(i)
        print 'upload finished'

    def reindex_catalog(self, url):
        _browser.open(url)
        ctrl = _browser.getControl('Title')
        ctrl.value = title
        ctrl = _browser.getControl('Annotation')
        ctrl.value = title
        ctrl = _browser.getControl('Body')
        ctrl.value = body
        ctrl = _browser.getControl(name='add_input_name')
        ctrl.value = title
        _browser.getControl(name='UPDATE_SUBMIT').click()


def main(argv):
    parseParameters(argv)
    #install_opener(_host, _username, _password)
    u = NewsUploader(_host, _addformurl, _storagedir)

def install_opener(host, username, password):
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(REALM, host, username, password)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

def parseParameters(argv):
    import getopt
    try:
         if len(argv) == 1:
             raise getopt.GetoptError('No arguments provided')
         opts, args = getopt.getopt(argv[1:], "o:u:p:a:s:hd", \
                                    ['host=',
                                     'username=',
                                     'password=',
                                     'addformurl=',
                                     'storagedir=',
                                     'help'])
    except getopt.GetoptError:
         usage()
         sys.exit(2)
    for opt, arg in opts:
        if opt in ('−h', '--help'):
            usage()
            sys.exit()
        elif opt == '−d':
            global _debug
            debug = 1
        elif opt in ('−o', '--host'):
            global _host
            _host = arg
        elif opt in ('−u', '--username'):
            global _username
            _username = arg
        elif opt in ('−p', '--password'):
            global _password
            _password = arg
        elif opt in ('−a', '--addformurl'):
            global _addformurl
            _addformurl = arg
        elif opt in ('−s', '--storagedir'):
            global _storagedir
            _storagedir = arg

def usage():
    print USAGE

if __name__ == '__main__':
    import sys
    main(sys.argv)