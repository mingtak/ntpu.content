# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from ntpu.content.config import StateZh_TW
from plone import api
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from email.mime.text import MIMEText
from Products.CMFPlone.utils import safe_unicode
from ntpu.content import MessageFactory as _


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def transition_check(item, event):
    if event.transition is None:
        return
    request = item.REQUEST

    if event.transition.getId() == 'toInReview':
        if item.assignInternalReviewer or \
           item.assignExternalReviewer1 or \
           item.assignExternalReviewer2 or \
           item.assignExternalReviewer3:
            api.portal.show_message(message=u'程序錯誤導致提交失敗，請檢查稿件目前狀態，確認提交程序正確.', request=request, type='error')
            raise

    if event.transition.getId() == 'assignInternal':
        if item.assignExternalReviewer1 or \
           item.assignExternalReviewer2 or \
           item.assignExternalReviewer3:
            api.portal.show_message(message=u'程序錯誤導致提交失敗，請檢查稿件目前狀態，確認提交程序正確.', request=request, type='error')
            raise
