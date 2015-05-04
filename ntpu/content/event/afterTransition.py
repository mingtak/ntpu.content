# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from ntpu.content.config import StateZh_TW
from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from email.mime.text import MIMEText
from ntpu.content import MessageFactory as _


def notifyChangeReviewState(emailList=[], article=None, event=None):
    newState = event.new_state.getId()
    oldState = event.old_state.getId()
    urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
    stateTag = "<p>狀態變更: 由 %s 變更為 %s</p>" % (StateZh_TW[oldState], StateZh_TW[newState])
    head = """
           <html><body><p>
             <strong>您好:</strong><br>
               這裏是運動研究期刊編輯部, 有一份關於稿件新的狀態更新通知您:<br>
             <p>
           """
    tail = """
           <hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件.</p>
           </body></html>
           """
    mailBody = MIMEText("%s%s%s%s" % (head, urlTag, stateTag, tail), 'html', 'utf-8')
    for siteAdmin in emailList:
        api.portal.send_email(
            recipient=siteAdmin[1],
            subject='%s 您好，運動研究期刊:投搞狀態更新通知' % siteAdmin[0],
            body='%s' % mailBody.as_string(),
        )


def getEmailList(item, event, groups):
    catalog = item.portal_catalog
    brain = catalog({'Type':'Profile', 'groups':groups})
    if len(brain) == 0:
        return
    emailList = []
    for profile in brain:
        emailList.append([profile.Title, profile.email])
    return emailList


@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToSiteAdministrator(item, event):
    emailList = getEmailList(item, event, 'Site Administrators')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)


@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToSuperEditor(item, event):
    #要寄的條件寫在這裏
    if True:
        return
    emailList = getEmailList(item, event, 'SuperEditor')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)


@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToInternalReviewer(item, event):
    #要寄的條件寫在這裏
    if True:
        return
    emailList = getEmailList(item, event, 'InternalReviewer')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)


@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToExternalReviewer(item, event):
    #要寄的條件寫在這裏
    if True:
        return
    emailList = getEmailList(item, event, 'ExternalReviewer')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)


@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToOwner(item, event):
    #要寄的條件寫在這裏
    if True:
        return
