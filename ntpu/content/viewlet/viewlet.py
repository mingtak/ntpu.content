# -*- coding: utf-8 -*-
from five import grok
from plone.app.layout.viewlets.interfaces import IBelowContentBody, IBelowContent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ntpu.content.article import IArticle
from ntpu.content.profile import IProfile
from plone import api


#grok.templatedir('template')
"""
  viewlet named rule: Function_ViewletManager_ContextInterface
"""

class Blind_IBelowContentBody_IArticle(grok.Viewlet):
    grok.viewletmanager(IBelowContentBody)
    grok.context(IArticle)
    template = ViewPageTemplateFile('template/blind.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class AdminDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/adminDesktop.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class SuperEditorDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/superEditorDesktop.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class ExternalReviewerDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/externalReviewerDesktop.pt')

    def render(self):
#        self.reviewStateCount()
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )

        self.waitingForReview = []
        backRef = self.getView.externalReviewerBackRef()
        for item in backRef:
#            import pdb; pdb.set_trace()
            if bool(item.assignExternalReviewer1) and item.assignExternalReviewer1.to_object == self.context:
                if not item.reviewConfirm1:
                    self.waitingForReview.append(item)
            if bool(item.assignExternalReviewer2) and item.assignExternalReviewer2.to_object == self.context:
                if not item.reviewConfirm2:
                    self.waitingForReview.append(item)
            if bool(item.assignExternalReviewer3) and item.assignExternalReviewer3.to_object == self.context:
                if not item.reviewConfirm3:
                    self.waitingForReview.append(item)
        return self.template()


class InternalReviewerDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/internalReviewerDesktop.pt')

    def reviewStateCount(self):
        # waitingAssignEx: 待指定委員
        self.waitingAssignEx = 0
        # waitingForReview: 審查中
        self.waitingForReview = 0
        # endReview: 審查完
        self.endReview = 0
        catalog = self.context.portal_catalog
        currentUserId = api.user.get_current().getId()
        profileBrain = catalog({'Type':'Profile', 'Creator':currentUserId})
        if len(profileBrain) == 0:
            return
        profile = profileBrain[0]
        brain = catalog({'Type':'Article',
                         'review_state':['internalAssigned', 'retrial'],
                         'assignInternalReviewer':profile.id})
#        import pdb; pdb.set_trace()
        if len(brain) == 0:
            return
        # 計算待指定委員
        for item in brain:
            count = 0
            if item.assignExternalReviewer1:
                count += 1
            if item.assignExternalReviewer2:
                count += 1
            if item.assignExternalReviewer3:
                count += 1
            if count < 2:
                self.waitingAssignEx += 1

        # 計算審查中, 審查完
        for item in brain:
            itemObj = item.getObject()
            yes, no = 0, 0
            if bool(item.assignExternalReviewer1) and bool(itemObj.reviewConfirm1):
                yes += 1
            elif bool(item.assignExternalReviewer1) and not bool(itemObj.reviewConfirm1):
                no += 1
            if bool(item.assignExternalReviewer2) and bool(itemObj.reviewConfirm2):
                yes += 1
            elif bool(item.assignExternalReviewer2) and not bool(itemObj.reviewConfirm2):
                no += 1
            if bool(item.assignExternalReviewer3) and bool(itemObj.reviewConfirm3):
                yes += 1
            elif bool(item.assignExternalReviewer3) and not bool(itemObj.reviewConfirm3):
                no += 1
            if no > 0:
                self.waitingForReview += 1
            if yes > 1 and no == 0:
                self.endReview += 1
        return

    def render(self):
        self.reviewStateCount()
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class ReviewState_IBelowContent_IArticle(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IArticle)
    template = ViewPageTemplateFile('template/reviewState.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class EditOrReview_IBelowContent_IArticle(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IArticle)
    template = ViewPageTemplateFile('template/editOrReview.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()


class ReviewResultForInternalReviewer_IBelowContent_IArticle(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IArticle)
    template = ViewPageTemplateFile('template/reviewResultForInternalReviewer.pt')

    def render(self):
        self.getView = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )
        return self.template()
