# -*- coding: utf-8 -*-
from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from email.mime.text import MIMEText
#from Products.CMFPlone.utils import safe_unicode
from ntpu.content.journal import IJournal
from ntpu.content.article import IArticle

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from ntpu.content import MessageFactory as _


grok.templatedir('template')


class ArticleList(grok.View):
    grok.context(Interface)
    grok.name('articleList')
    grok.template('articleList')

    def update(self):
        context = self.context
        request = context.REQUEST
        catalog = context.portal_catalog
        state = getattr(request, 'state', None)
        if state is None:
            return request.respnse.redirect('/')
        self.brain = catalog({'Type':'Article', 'review_state':state}, sort_on='created', sort_order='reverse')
        return
