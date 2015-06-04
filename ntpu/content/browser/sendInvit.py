# -*- coding: utf-8 -*-
from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from email.mime.text import MIMEText
#from Products.CMFPlone.utils import safe_unicode
from ntpu.content.journal import IJournal
from ntpu.content.article import IArticle
from ntpu.content.profile import IProfile

from ntpu.content.event.modifiedArticle import creatPara, sendMail

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from ntpu.content import MessageFactory as _


grok.templatedir('template')


class SendInvite(grok.View):
    grok.context(IArticle)
    grok.name('sendInvite')

    def render(self):
        portal = api.portal.get()
        context = self.context
        request = context.REQUEST
        response = context.REQUEST.response
        reviewer = request['reviewer']

        if reviewer == "assignExternalReviewer1":
            assignExternalReviewer1 = context.assignExternalReviewer1
            invitEmail1 = context.invitEmail1
            acceptInvit1 = context.acceptInvit1
            para = creatPara()
            email = context.assignExternalReviewer1.to_object.email
            context.invitEmail1 = para

        if reviewer == "assignExternalReviewer2":
            assignExternalReviewer2 = context.assignExternalReviewer2
            invitEmail2 = context.invitEmail2
            acceptInvit2 = context.acceptInvit2
            para = creatPara()
            email = context.assignExternalReviewer2.to_object.email
            context.invitEmail2 = para

        if reviewer == "assignExternalReviewer3":
            assignExternalReviewer3 = context.assignExternalReviewer3
            invitEmail3 = context.invitEmail3
            acceptInvit3 = context.acceptInvit3
            para = creatPara()
            email = context.assignExternalReviewer3.to_object.email
            context.invitEmail3 = para

        url = '%s/@@inviteReview?para=%s' % (portal.absolute_url(), para)
        sendMail(obj=context, url=url, email=email)

        message = _(u"Invite email already sent.")
        api.portal.show_message(
            message=message,
            request=context.REQUEST,
            type='info'
        )
        response.redirect(context.absolute_url())
        context.reindexObject()
