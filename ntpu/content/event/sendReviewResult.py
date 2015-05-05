# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from plone import api
#from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from ntpu.content.article import IArticle
#from Products.CMFPlone import utils
from email.mime.text import MIMEText


def notifyAuthor(article):
    email = article.owner_info()['id']
    urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
    head = """
           <html><body><p>
             <strong>敬愛的作者</strong>您好:<br>
               這裏是運動研究期刊編輯部, 有一份關於稿件新的審查狀態更新通知您:<br>
             <p>
           """
    tail = """
           <hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:02-XXXXXXXX</p>
           </body></html>
           """
    mailBody = MIMEText("%s%s%s" % (head, urlTag, tail), 'html', 'utf-8')
    api.portal.send_email(
        recipient=email,
        subject='運動研究期刊編輯部:審查狀態更新通知',
        body='%s' % mailBody.as_string(),
    )


def notifyReviewState(article):
    email = article.assignInternalReviewer.to_object.email
    urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
    head = """
           <html><body><p>
             <strong>敬愛的教授</strong>您好:<br>
               這裏是運動研究期刊編輯部, 有一份關於稿件新的審查狀態更新通知您:<br>
             <p>
           """
    tail = """
           <hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:02-XXXXXXXX</p>
           </body></html>
           """
    mailBody = MIMEText("%s%s%s" % (head, urlTag, tail), 'html', 'utf-8')
    api.portal.send_email(
        recipient=email,
        subject='運動研究期刊編輯部:審查狀態更新通知',
        body='%s' % mailBody.as_string(),
    )


# 暫時不寄給作者了
""" @grok.subscribe(IArticle, IObjectModifiedEvent) """
def sendReviewResult(obj, event):
#    import pdb; pdb.set_trace()
    portal = api.portal.get()
    currentUserId = api.user.get_current().getId()
    externalReviewerList = []
    if obj.assignExternalReviewer1 is not None:
        externalReviewerList.append(obj.assignExternalReviewer1.to_object.owner_info()['id'])
    if obj.assignExternalReviewer2 is not None:
        externalReviewerList.append(obj.assignExternalReviewer2.to_object.owner_info()['id'])
    if obj.assignExternalReviewer3 is not None:
        externalReviewerList.append(obj.assignExternalReviewer3.to_object.owner_info()['id'])
    if currentUserId not in externalReviewerList:
        return

    reviewResult = 0
    if obj.acceptOrReject1 is not None:
        reviewResult += 1
    if obj.acceptOrReject2 is not None:
        reviewResult += 1
    if obj.acceptOrReject3 is not None:
        reviewResult += 1

    if reviewResult > 1:
        notifyReviewState(article=obj)
        notifyAuthor(article=obj)
