from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


grok.templatedir('template')

class InviteReview(grok.View):
    grok.context(Interface)
    grok.name('inviteReview')
    grok.template('inviteReview')

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
