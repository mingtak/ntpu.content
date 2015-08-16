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

from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from ntpu.content import MessageFactory as _


grok.templatedir('template')


class ArticleList(grok.View):
#    grok.context(Interface)
    grok.context(IProfile)
    grok.name('articleList')
    grok.template('articleList')

    def getRoles(self):
        return api.user.get_roles()

    def update(self):
        context = self.context
        request = context.REQUEST
        catalog = context.portal_catalog
        state = getattr(request, 'state', None)
        if state is None:
            return request.response.redirect('/')
        self.brain = catalog({'Type':'Article', 'review_state':state}, sort_on='created', sort_order='reverse')
#        import pdb;pdb.set_trace()
        return


# 責編的桌面列表
class ArticleListForInter(grok.View):
    grok.context(IProfile)
    grok.name('articleListForInter')
    grok.template('articleListForInter')
    # list 待指定審查委員
    def update(self):
        self.waitingAssignEx = []
        self.waitingForReview = []
        self.endReview = []
        currentUserId = api.user.get_current().getId()

        view = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )

        backRef = view.internalReviewerBackRef()

        if len(backRef) == 0:
            return
        # 計算待指定委員
        for item in backRef:
            count = 0
            if item.assignExternalReviewer1:
                count += 1
            if item.assignExternalReviewer2:
                count += 1
            if item.assignExternalReviewer3:
                count += 1
            if count < 2:
                self.waitingAssignEx.append(item)

        # 計算審查中, 審查完
        for item in backRef:
#            itemObj = item.getObject()
            yes, no = 0, 0
            if bool(item.assignExternalReviewer1) and bool(item.acceptOrReject1):
                yes += 1
            elif bool(item.assignExternalReviewer1) and not bool(item.acceptOrReject1):
                no += 1
            if bool(item.assignExternalReviewer2) and bool(item.acceptOrReject2):
                yes += 1
            elif bool(item.assignExternalReviewer2) and not bool(item.acceptOrReject2):
                no += 1
            if bool(item.assignExternalReviewer3) and bool(item.acceptOrReject3):
                yes += 1
            elif bool(item.assignExternalReviewer3) and not bool(item.acceptOrReject3):
                no += 1
            if no > 0:
                self.waitingForReview.append(item)
            if yes > 1 and no == 0:
                self.endReview.append(item)
        return


# 審查委員的桌面列表
class ArticleListForExter(grok.View):
    grok.context(IProfile)
    grok.name('articleListForExter')
    grok.template('articleListForExter')
    # list 待指定審查委員
    def update(self):
        self.waitingAssignEx = []
        self.waitingForReview = []
        self.endReview = []
        currentUserId = api.user.get_current().getId()

        view = api.content.get_view(
            name='view',
            context=self.context,
            request=self.context.REQUEST,
        )

        self.waitingForReview = []
        backRef = view.externalReviewerBackRef()
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

