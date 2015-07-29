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


class ReviewConfirm(grok.View):
    grok.context(IArticle)
    grok.name('reviewConfirm')

    def render(self):
        context = self.context
        request = context.REQUEST
        redirect = request.response.redirect
        currentUserId = api.user.get_current().getId()
        if context.assignExternalReviewer1 is not None:
            externalReviewer1_Id = context.assignExternalReviewer1.to_object.owner_info()['id']
            if currentUserId == externalReviewer1_Id:
                if context.acceptOrReject1 is None or (context.externalReviewerComment1 is None and context.reviewCommentAttached1 is None):
                    api.portal.show_message(message=_(u'No Review result yet.'), request=request, type='error')
                    context.reviewConfirm1 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return
                if not context.scoreR1Q1 or not context.scoreR1Q2 or not context.scoreR1Q3 or not context.scoreR1Q4:
                    api.portal.show_message(message=_(u'No Review score yet.'), request=request, type='error')
                    context.reviewConfirm1 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return

                context.reviewConfirm1 = True
                api.portal.show_message(message=_(u'Successfully submitted for review.'), request=request, type='info')

        if context.assignExternalReviewer2 is not None:
            externalReviewer2_Id = context.assignExternalReviewer2.to_object.owner_info()['id']
            if currentUserId == externalReviewer2_Id:
                if context.acceptOrReject2 is None or (context.externalReviewerComment2 is None and context.reviewCommentAttached2 is None):
                    api.portal.show_message(message=_(u'No Review result yet.'), request=request, type='error')
                    context.reviewConfirm2 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return
                if not context.scoreR2Q1 or not context.scoreR2Q2 or not context.scoreR2Q3 or not context.scoreR2Q4:
                    api.portal.show_message(message=_(u'No Review score yet.'), request=request, type='error')
                    context.reviewConfirm1 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return

                context.reviewConfirm2 = True
                api.portal.show_message(message=_(u'Successfully submitted for review.'), request=request, type='info')

        if context.assignExternalReviewer3 is not None:
            externalReviewer3_Id = context.assignExternalReviewer3.to_object.owner_info()['id']
            if currentUserId == externalReviewer3_Id:
                if context.acceptOrReject3 is None or (context.externalReviewerComment3 is None and context.reviewCommentAttached3 is None):
                    api.portal.show_message(message=_(u'No Review result yet.'), request=request, type='error')
                    context.reviewConfirm3 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return
                if not context.scoreR3Q1 or not context.scoreR3Q2 or not context.scoreR3Q3 or not context.scoreR3Q4:
                    api.portal.show_message(message=_(u'No Review score yet.'), request=request, type='error')
                    context.reviewConfirm1 = None
                    context.reindexObject()
                    redirect(context.absolute_url())
                    return

                context.reviewConfirm3 = True
                api.portal.show_message(message=_(u'Successfully submitted for review.'), request=request, type='info')

        notify(ObjectModifiedEvent(context))
        context.reindexObject()
        redirect(context.absolute_url())
        return


class DownloadFile(grok.View):
    grok.context(IJournal)
    grok.name('downloadfile')

    def render(self):
        context = self.context
        context.downloadCount += 1
        response = context.REQUEST.response
        string = '%s/@@download/attachFile/%s' % (context.absolute_url(), context.attachFile.filename)
        string = string.encode('utf-8')
        response.redirect(string)


class InviteReview(grok.View):
    grok.context(Interface)
    grok.name('inviteReview')
    grok.template('inviteReview')

    def notifyAcceptMail(self, article, accepter):
#        catalog = salf.context.portal_catalog
#        brain = catalog({'Type':'Profile', 'groups':'Site Administrators'})
#        if len(brain) == 0:
#            return
#        email = []
#        for item in brain:
#            email.append(item.email)
        email = article.assignInternalReviewer.to_object.email
        urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
        accepter="<p>委員姓名: %s</p>" % accepter.encode('utf-8')
        head = """
               <html><body><p>
                 <strong>敬愛的教授</strong>您好:<br>
                   這裏是臺北市立大學研發處學術出版組, 有一份關接受擔任審查委員的邀請通知如下:<br>
                 <p>
               """
        tail = """
               <hr>
               <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:（02）2871-8288轉7808 陸小姐</p>
               </body></html>
               """
        mailBody = MIMEText("%s%s%s%s" % (head, urlTag, accepter, tail), 'html', 'utf-8')
        api.portal.send_email(
            recipient=email,
            subject='臺北市立大學研發處學術出版組:接受擔任審查委員通知信件',
            body='%s' % mailBody.as_string()
        )

    def notifyRejectMail(self, article, rejecter):
        email = article.assignInternalReviewer.to_object.email
        urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
        rejecter="<p>委員姓名: %s</p>" % rejecter.encode('utf-8')
        head = """
               <html><body><p>
                 <strong>敬愛的教授</strong>您好:<br>
                   這裏是臺北市立大學研發處學術出版組, 有一份關於拒絕擔任審查委員的邀請通知如下:<br>
                 <p>
               """
        tail = """
               <hr>
               <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:（02）2871-8288轉7808 陸小姐</p>
               </body></html>
               """
        mailBody = MIMEText("%s%s%s%s" % (head, urlTag,rejecter, tail), 'html', 'utf-8')
        api.portal.send_email(
            recipient=email,
            subject='臺北市立大學研發處學術出版組:拒絕擔任審查委員通知信件',
            body='%s' % mailBody.as_string()
        )


    def update(self):
        context = self.context
        request = context.REQUEST
        catalog = context.portal_catalog
        adminId = api.user.get_users(groupname='Site Administrators')[0].getProperty('email')
        with api.env.adopt_user(username=adminId):
            while True:
                brain = catalog(invitEmail1=request['para'])
                if len(brain)>0:
                    article = brain[0].getObject()
                    profile = article.assignExternalReviewer1.to_object
                    userId = profile.email
                    if request.has_key('accept'):
                        accepter = article.assignExternalReviewer1.to_object.myName
                        self.notifyAcceptMail(article=article, accepter=accepter)
                        article.acceptInvit1 = True
                        article.invitEmail1 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
#                        return
                    elif request.has_key('reject'):
                        rejecter = article.assignExternalReviewer1.to_object.myName
                        self.notifyRejectMail(article=article, rejecter=rejecter)
                        article.assignExternalReviewer1 = None
                        article.invitEmail1 = None
                        article.acceptInvit1 = None
                        article.reindexObject()
                        request.response.redirect('/')
                        return
                    break
                brain = catalog(invitEmail2=request['para']) 
                if len(brain)>0:
                    article = brain[0].getObject()
                    profile = article.assignExternalReviewer2.to_object
                    userId = profile.email
                    if request.has_key('accept'):
                        accepter = article.assignExternalReviewer2.to_object.myName
                        self.notifyAcceptMail(article=article, accepter=accepter)
                        article.acceptInvit2 = True
                        article.invitEmail2 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
#                        return
                    elif request.has_key('reject'):
                        rejecter = article.assignExternalReviewer2.to_object.myName
                        self.notifyRejectMail(article=article, rejecter=rejecter)
                        article.assignExternalReviewer2 = None
                        article.invitEmail2 = None
                        article.acceptInvit2 = None
                        article.reindexObject()
                        request.response.redirect('/')
                        return
                    break
                brain = catalog(invitEmail3=request['para']) 
                if len(brain)>0:
                    article = brain[0].getObject()
                    profile = article.assignExternalReviewer3.to_object
                    userId = profile.email
                    if request.has_key('accept'):
                        accepter = article.assignExternalReviewer3.to_object.myName
                        self.notifyAcceptMail(article=article, accepter=accepter)
                        article.acceptInvit3 = True
                        article.invitEmail3 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
#                        break
#                        return
                    elif request.has_key('reject'):
                        rejecter = article.assignExternalReviewer3.to_object.myName
                        self.notifyRejectMail(article=article, rejecter=rejecter)
                        article.assignExternalReviewer3 = None
                        article.invitEmail3 = None
                        article.acceptInvit3 = None
                        article.reindexObject()
                        request.response.redirect('/')
                        return
                    break
                request.response.redirect('/')
                return
        self.profile = profile
        self.brain = brain
        context.acl_users.session._setupSession(userId.encode("utf-8"), self.context.REQUEST.RESPONSE)
        return
