# -*- coding: utf-8 -*-
from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from ntpu.content.config import StateZh_TW
from plone import api
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from email.mime.text import MIMEText
from Products.CMFPlone.utils import safe_unicode
from ntpu.content import MessageFactory as _


def notifyChangeReviewState(emailList=[], article=None, event=None):
    newState = event.new_state.getId()
    oldState = event.old_state.getId()
    urlTag = u"<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
    stateTag = u"<p>狀態變更: 由 %s 變更為 %s</p>" % (StateZh_TW[oldState], StateZh_TW[newState])
    head = """
           <html><body><p>
             <strong>您好:</strong><br>
               這裏是臺北市立大學研發處學術出版組, 有一份關於稿件新的狀態更新通知您:<br>
             <p>
           """
    tail = """
           <hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件.</p>
           </body></html>
           """
    head = safe_unicode(head)
    tail = safe_unicode(tail)
    mailBody = MIMEText("%s%s%s%s" % (head, urlTag, stateTag, tail), 'html', 'utf-8')
    for siteAdmin in emailList:
        api.portal.send_email(
            recipient=siteAdmin[1],
            subject='%s 您好，臺北市立大學研發處學術出版組:投搞狀態更新通知' % siteAdmin[0],
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
    if event.old_state.getId() == event.new_state.getId():
        return
    emailList = getEmailList(item, event, 'Site Administrators')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)

@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToSuperEditor(item, event):
    if event.new_state.getId() not in ['accepted', 'rejected', 'inReview']:
        return
    emailList = getEmailList(item, event, 'SuperEditor')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)

@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToInternalReviewer(item, event):
    #要寄的條件寫在這裏
    if event.new_state.getId() not in ['internalAssigned']:
        return
    emailList = getEmailList(item, event, 'InternalReviewer')
    if emailList == []:
        return
    notifyChangeReviewState(emailList=emailList, article=item, event=event)

@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToExternalReviewer(item, event):
    #要寄的條件寫在這裏
    if event.new_state.getId() != 'retrial':
        return

    emailList = []
    if item.acceptOrReject1 == 'MR':
        item.externalReviewerComment1 = None
        item.reviewCommentAttached1 = None
        item.reviewConfirm1 = None
        item.acceptOrReject1 = None
        profile = item.assignExternalReviewer1.to_object
        emailList.append([profile.Title(), profile.email])
    if item.acceptOrReject2 == 'MR':
        item.externalReviewerComment2 = None
        item.reviewCommentAttached2 = None
        item.reviewConfirm2 = None
        item.acceptOrReject2 = None
        profile = item.assignExternalReviewer2.to_object
        emailList.append([profile.Title(), profile.email])
    if item.acceptOrReject3 == 'MR':
        item.externalReviewerComment3 = None
        item.reviewCommentAttached3 = None
        item.reviewConfirm3 = None
        item.acceptOrReject3 = None
        profile = item.assignExternalReviewer3.to_object
        emailList.append([profile.Title(), profile.email])

    if emailList == []:
        return
    item.reindexObject()
    notifyChangeReviewState(emailList=emailList, article=item, event=event)

@grok.subscribe(IArticle, IAfterTransitionEvent)
def mailToOwner(item, event):
    #要寄的條件寫在這裏
    if event.old_state.getId() == event.new_state.getId():
        return
    if event.new_state.getId() not in ['draft', 'modifyThenReview']:
        return
    catalog = item.portal_catalog
    profileBrain = catalog({'Type':'Profile', 'Creator':item.owner_info()['id']})
    if len(profileBrain) == 0:
        return
    profile = profileBrain[0]
    emailList = [[profile.Title, profile.email],]
    notifyChangeReviewState(emailList=emailList, article=item, event=event)
    return

@grok.subscribe(IArticle, IAfterTransitionEvent)
def retractToOwner(item, event):
    #退件寄信給作者
    if event.transition is None:
        return
    if event.transition.getId() != 'retract':
        return

    urlTag = u"<p>稿件連結: <a href='%s'>%s</a></p>" % (item.absolute_url(), item.absolute_url())
    reasonTag = u"<p>退稿理由: %s</p>" % (item.retractReason)
    head = """
           <html><body><p>
             <strong>您好:</strong><br>
               這裏是臺北市立大學研發處學術出版組, 有一份關於稿件的退稿通知:<br>
             <p>
           """
    tail = """
           <hr>
           <p>本郵件由系統直接發出，請勿直接回覆本信件.</p>
           </body></html>
           """
    head = safe_unicode(head)
    tail = safe_unicode(tail)
    mailBody = MIMEText("%s%s%s%s" % (head, urlTag, reasonTag, tail), 'html', 'utf-8')

    catalog = item.portal_catalog
    profileBrain = catalog({'Type':'Profile', 'Creator':item.owner_info()['id']})
    if len(profileBrain) == 0:
        return
    profile = profileBrain[0].getObject()

    api.portal.send_email(
        recipient=profile.email,
        subject=u'%s 您好，臺北市立大學研發處學術出版組:投搞狀態更新通知' % safe_unicode(profile.myName),
        body='%s' % mailBody.as_string(),
    )

    item.retractReason = None
    item.reindexObject()
    return


@grok.subscribe(IArticle, IAfterTransitionEvent)
def notifySubmiitedSuccess(item, event):
    #提交成功訊息
    request = item.REQUEST
    if event.transition is None:
        return
    if event.transition.getId() != 'submitting':
        return
    
    api.portal.show_message(message=u'您的稿件已提交成功.', request=request)


@grok.subscribe(IArticle, IAfterTransitionEvent)
def give_sn(item, event):
    if event.transition is None:
        return
    if event.transition.getId() != 'submitting':
        return

    catalog = item.portal_catalog
    brain = catalog({'Type':'Article'}, sort_on='sn', sort_order='reverse')
    if not brain[0].sn:
        item.sn = 1
    else:
        item.sn = brain[0].sn + 1
    item.reindexObject()


@grok.subscribe(IArticle, IAfterTransitionEvent)
def check_same_title(item, event):
    if event.transition is None:
        return
    if event.transition.getId() != 'submitting':
        return

    request = item.REQUEST
    catalog = item.portal_catalog
    brain = catalog({'Type':'Article',
                     'articleTitleC':item.articleTitle,
                     'articleTitleE':item.engTitle,
                     'review_state':[
                         'accepted',
                         'inReview',
                         'internalAssigned',
                         'modifyThenReview',
                         'reSubmitted',
                         'rejected',
                         'retrial',
                         'submitted']},
                    sort_on='sn', sort_order='reverse')

    if len(brain) > 1:
        with api.env.adopt_roles(['Site Administrator', 'Manager']):
            item.sn = None
            api.portal.show_message(message=u'你有一份同名稿件已經投稿待審，請勿重複投搞.', request=request, type='warning')
            api.content.transition(obj=item, transition='retract')
            item.reindexObject()

