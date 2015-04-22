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

    def update(self):
        DefaultEditForm.update(self)

    def updateWidgets(self):
        super(ArticleEditForm, self).updateWidgets()
        view = api.content.get_view(name='view', context=self.context, request=self.request)
        selfBrain = view.getSelfBrain()
        if len(selfBrain) == 0:
            return
        currentUserId = api.user.get_current().getId()

        if 'Site Administrator' in view.getRoles():
            return

        if selfBrain.reviewResults is None or len(selfBrain.reviewResults) < 2:
            for group in self.groups:
                for key in group.fields.keys():
                    if key in ['assignExtraReviewer',]:
                       group.fields[key].mode = 'hidden'
        elif len(selfBrain.reviewResults) == 2:
            for group in self.groups:
                for key in group.fields.keys():
                    if key in ['assignExternalReviewer',]:
                        group.fields[key].mode = 'display'
        if selfBrain.reviewResults is not None:
            for comment in selfBrain.reviewResults:
                if currentUserId == comment[0]:
                    for group in self.groups:
                        for key in group.fields.keys():
                            if key in ['acceptOrReject', 'externalReviewerComment']:
                                group.fields[key].mode = 'hidden'
                    group.description = 'You are already reviewd this paper.'
        if not view.checkIdInReviewerList():
            for group in self.groups:
                for key in group.fields.keys():
                    if key in ['acceptOrReject', 'externalReviewerComment']:
                        group.fields[key].mode = 'hidden'


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




