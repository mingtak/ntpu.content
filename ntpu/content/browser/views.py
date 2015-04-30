# -*- coding: utf-8 -*-
from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from email.mime.text import MIMEText
#from Products.CMFPlone.utils import safe_unicode
from ntpu.content.journal import IJournal


grok.templatedir('template')

class DownloadFile(grok.View):
    grok.context(IJournal)
    grok.name('downloadfile')

    def render(self):
        context = self.context
        context.downloadCount += 1
        response = context.REQUEST.response
        string = '%s/@@download/attachFile/%s' % (context.absolute_url(), context.attachFile.filename)
        response.redirect(string)


class InviteReview(grok.View):
    grok.context(Interface)
    grok.name('inviteReview')
    grok.template('inviteReview')

    def notifyRejectMail(self, article, rejecter):
        email = article.assignInternalReviewer.to_object.email
        urlTag = "<p>稿件連結: <a href='%s'>%s</a></p>" % (article.absolute_url(), article.absolute_url())
        rejecter="<p>委員姓名: %s</p>" % rejecter.encode('utf-8')
        head = """
               <html><body><p>
                 <strong>敬愛的教授</strong>您好:<br>
                   這裏是運動研究期刊編輯部, 有一份關於拒絕擔任審查委員的邀請通知如下:<br>
                 <p>
               """
        tail = """
               <hr>
               <p>本郵件由系統直接發出，請勿直接回覆本信件，若有相關疑問，請與本刊聯絡，電話:02-XXXXXXXX</p>
               </body></html>
               """
        mailBody = MIMEText("%s%s%s%s" % (head, urlTag,rejecter, tail), 'html', 'utf-8')
        api.portal.send_email(
            recipient=email,
            subject='運動研究期刊編輯部:拒絕擔任審查委員通知信件',
            body='%s' % mailBody.as_string()
        )


    def update(self):
        context = self.context
        request = context.REQUEST
        catalog = context.portal_catalog
        adminId = api.user.get_users(groupname='Site Administrators')[0].getId()
        with api.env.adopt_user(username=adminId):
            while True:
                brain = catalog(invitEmail1=request['para'])
                if len(brain)>0:
                    article = brain[0].getObject()
                    profile = article.assignExternalReviewer1.to_object
                    userId = profile.email
                    if request.has_key('accept'):
                        article.acceptInvit1 = True
                        article.invitEmail1 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
                        return
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
                        article.acceptInvit2 = True
                        article.invitEmail2 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
                        return
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
                        article.acceptInvit3 = True
                        article.invitEmail3 = None
                        article.reindexObject()
                        request.response.redirect(brain[0].getURL())
                        return
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
