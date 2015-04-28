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


def creatPara():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(60))


def sendMail(obj, url, email):
    urlTag = "<a href='%s'>%s</a>" % (url, url)
    head = """
           <html><body><p>
             <strong>敬愛的教授</strong>您好:<br>
               這裏是運動研究期刊編輯部, 我們有一份稿件要邀請您擔任審查委員<br>
               請您點擊以下連結，回覆我們是否同意擔任本次審查委員</p>
           """
    tail = """
           <p>感謝您的回覆</p><hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:02-XXXXXXXX</p>
           </body></html>
           """
    mailBody = MIMEText("%s%s%s" % (head, urlTag, tail), 'html', 'utf-8')

    api.portal.send_email(
        recipient=email,
        subject='運動研究期刊編輯部:邀請擔任審查委員',
        body='%s' % mailBody.as_string()
    )
    return


@grok.subscribe(IArticle, IObjectModifiedEvent)
def modifyInvitEmail(obj, event):
    if obj.assignExternalReviewer1 is None:
        obj.acceptInvit1 = None
        obj.invitEmail1 = None
    if obj.assignExternalReviewer2 is None:
        obj.acceptInvit2 = None
        obj.invitEmail2 = None
    if obj.assignExternalReviewer3 is None:
        obj.acceptInvit3 = None
        obj.invitEmail3 = None
    obj.reindexObject()



@grok.subscribe(IArticle, IObjectModifiedEvent)
def sendInvitEmail(obj, event):
#    import pdb; pdb.set_trace()
    portal = api.portal.get()
    if obj.assignExternalReviewer1 is not None and obj.invitEmail1 is None and obj.acceptInvit1 is None:
        para = creatPara()
        url = '%s/@@inviteReview?para=%s' % (portal.absolute_url(), para)
        email = obj.assignExternalReviewer1.to_object.email
        obj.invitEmail1 = para
        sendMail(obj=obj,url=url, email=email)

    if obj.assignExternalReviewer2 is not None and obj.invitEmail2 is None and obj.acceptInvit2 is None:
        para = creatPara()
        url = '%s/@@inviteReview?para=%s' % (portal.absolute_url(), para)
        email = obj.assignExternalReviewer2.to_object.email
        obj.invitEmail2 = para
        sendMail(obj=obj,url=url, email=email)

    if obj.assignExternalReviewer3 is not None and obj.invitEmail3 is None and obj.acceptInvit3 is None:
        para = creatPara()
        url = '%s/@@inviteReview?para=%s' % (portal.absolute_url(), para)
        email = obj.assignExternalReviewer3.to_object.email
        obj.invitEmail3 = para
        sendMail(obj=obj,url=url, email=email)

    obj.reindexObject()
