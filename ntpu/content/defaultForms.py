from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.dexterity.browser.edit import DefaultEditForm, DefaultEditView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form.interfaces import HIDDEN_MODE

from zope.component import getMultiAdapter
from plone import api

#from zope.interface import alsoProvides, Interface

#from ntpu.content.article import IDemoWidget
from plone.directives import dexterity, form

from ntpu.content import MessageFactory as _


def getLanguage(self):
    context = self.context
    portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
    current_language = portal_state.language()
    return current_language


class AddForm(DefaultAddForm):
    template = ViewPageTemplateFile('template/addForm.pt')


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm):
    template = ViewPageTemplateFile('template/editForm.pt')


class EditView(DefaultEditView):
    form = EditForm



##### Edit form, use updateWidgets to turn hidden/display
class ArticleEditForm(DefaultEditForm):
    template = ViewPageTemplateFile('template/editForm.pt')

    def getReviewerId(self, reviewerItem):
        """ reviewerItem like articleItem.assignExternalReviewer2 """
        if reviewerItem is None:
            return None
        else:
            return reviewerItem.to_object.owner_info()['id']

    def hiddenFields(self, label, mode, keys=[]):
        for group in self.groups:
            if group.label == label:
                for key in group.fields.keys():
                    if key in keys:
                        group.fields[key].mode = mode

    def hiddenModifySubmission(self, articleItem):
        reviewResults = 0
        if articleItem.acceptOrReject1 is not None:
            reviewResults += 1
        if articleItem.acceptOrReject2 is not None:
            reviewResults += 1
        if articleItem.acceptOrReject3 is not None:
            reviewResults += 1
        if reviewResults > 1:
            for group in self.groups:
                if group.label == 'Manuscript file':
                    for key in group.fields.keys():
                        if key in ['modifySubmission']:
                            group.fields[key].mode = None
                            group.description = _(u"Please upload modify submission and modified article.")

    def update(self):
        DefaultEditForm.update(self)

    def updateWidgets(self):
        super(ArticleEditForm, self).updateWidgets()
        view = api.content.get_view(name='view', context=self.context, request=self.request)
        selfBrain = view.getSelfBrain()


        if len(selfBrain) == 0:
            return

        if 'Site Administrator' in view.getRoles():
            return


        currentUserId = api.user.get_current().getId()
        articleItem = selfBrain.getObject()
        reviewer_1_id = self.getReviewerId(articleItem.assignExternalReviewer1)
        reviewer_2_id = self.getReviewerId(articleItem.assignExternalReviewer2)
        reviewer_3_id = self.getReviewerId(articleItem.assignExternalReviewer3)

        if articleItem.assignExternalReviewer1 is not None and articleItem.acceptInvit1 != False:
            label = "Review State"
            keys = ['assignExternalReviewer1']
            self.hiddenFields(label=label, mode="display", keys=keys)

        if articleItem.assignExternalReviewer2 is not None and articleItem.acceptInvit2 != False:
            label = "Review State"
            keys = ['assignExternalReviewer2']
            self.hiddenFields(label=label, mode="display", keys=keys)

        if articleItem.assignExternalReviewer3 is not None and articleItem.acceptInvit3 != False:
            label = "Review State"
            keys = ['assignExternalReviewer1']
            self.hiddenFields(label=label, mode="display", keys=keys)

        if currentUserId != reviewer_1_id:
            label = "Review State"
            keys = ['acceptOrReject1',
                    'externalReviewerComment1',
                    'reviewCommentAttached1',]
            self.hiddenFields(label=label, mode="hidden", keys=keys)

        if currentUserId != reviewer_2_id:
            label = "Review State"
            keys = ['acceptOrReject2',
                    'externalReviewerComment2',
                    'reviewCommentAttached2',]
            self.hiddenFields(label=label, mode="hidden", keys=keys)

        if currentUserId != reviewer_3_id:
            label = "Review State"
            keys = ['acceptOrReject3',
                    'externalReviewerComment3',
                    'reviewCommentAttached3',]
            self.hiddenFields(label=label, mode="hidden", keys=keys)

        self.hiddenModifySubmission(articleItem)


class ArticleEditView(DefaultEditView):
    form = ArticleEditForm


##### Add form, use updateWidgets to turn hidden/display
class ArticleAddForm(DefaultAddForm):
    template = ViewPageTemplateFile('template/addForm.pt')

    def update(self):
        DefaultAddForm.update(self)
#        import pdb; pdb.set_trace()

    def updateWidgets(self):
        super(ArticleAddForm, self).updateWidgets()
#        if not api.user.is_anonymous() and 'Manager' not in api.user.get_roles():
#        self.widgets['submittingFrom'].disabled = True
        currentLanguage = getLanguage(self)
        if currentLanguage == 'en-us':
            for group in self.groups:
                for key in group.fields.keys():
                    if key in ['engTitle', 'engKeywords', 'engAbstract',]:
                       group.fields[key].mode = 'hidden'
        for group in self.groups:
            if group.label == 'Review State':
#                group.label = ''
#                group = None
                for key in group.fields.keys():
                    group.fields[key].mode = 'hidden'

        return


class ArticleAddView(DefaultAddView):
    form = ArticleAddForm









##### Edit form, use updateWidgets to turn hidden/display
class AuthorEditForm(DefaultEditForm):
    template = ViewPageTemplateFile('template/editForm.pt')

    def update(self):
        DefaultEditForm.update(self)

    def updateWidgets(self):
        super(AuthorEditForm, self).updateWidgets()

class AuthorEditView(DefaultEditView):
    form = AuthorEditForm


##### Add form, use updateWidgets to turn hidden/display
class AuthorAddForm(DefaultAddForm):
    template = ViewPageTemplateFile('template/addForm.pt')

    def update(self):
        DefaultAddForm.update(self)
#        import pdb; pdb.set_trace()

    def updateWidgets(self):

        super(AuthorAddForm, self).updateWidgets()
#        if not api.user.is_anonymous() and 'Manager' not in api.user.get_roles():
#        self.widgets['submittingFrom'].disabled = True
        currentLanguage = getLanguage(self)
        if currentLanguage == 'en-us':
            for group in self.groups:
                for key in group.fields.keys():
                    if key in ['IAuthorInformation.authorNameC', 'IAuthorInformation.institutionC', 'IAuthorInformation.titleC']:
                       group.fields[key].mode = 'hidden'

        return


class AuthorAddView(DefaultAddView):
    form = AuthorAddForm




