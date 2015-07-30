# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone import api
#from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from ntpu.content.article import IArticle
from Products.CMFPlone import utils
import random
import string
from email.mime.text import MIMEText
from Products.CMFPlone.utils import safe_unicode
from datetime import datetime


@grok.subscribe(IArticle, IObjectModifiedEvent)
def logEvent(obj, event):

    currentUser = api.user.get_current()
    currentUserId = currentUser.getId()

    log = ''
    if obj.assignExternalReviewer1 and obj.assignExternalReviewer1.to_object.owner_info()['id'] == currentUserId:
        name = safe_unicode(obj.assignExternalReviewer1.to_object.myName)
        date = safe_unicode(datetime.now().strftime('%Y / %m / %d'))
        result = safe_unicode(str(obj.acceptOrReject1))
        log = '%s, %s, %s' % (name, date, result)

    if obj.assignExternalReviewer2 and obj.assignExternalReviewer2.to_object.owner_info()['id'] == currentUserId:
        name = safe_unicode(obj.assignExternalReviewer2.to_object.myName)
        date = safe_unicode(datetime.now().strftime('%Y / %m / %d'))
        result = safe_unicode(str(obj.acceptOrReject2))
        log = '%s, %s, %s' % (name, date, result)

    if obj.assignExternalReviewer3 and obj.assignExternalReviewer3.to_object.owner_info()['id'] == currentUserId:
        name = safe_unicode(obj.assignExternalReviewer3.to_object.myName)
        date = safe_unicode(datetime.now().strftime('%Y / %m / %d'))
        result = safe_unicode(str(obj.acceptOrReject3))
        log = '%s, %s, %s' % (name, date, result)


    if log and obj.logText:
        obj.logText += '%s <br/>' % log
    elif log:
        obj.logText = '%s <br/>' % log
