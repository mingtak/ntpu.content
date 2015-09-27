from five import grok
from plone import api
from plone.supermodel import model
from plone.directives import form

from z3c.form import button, field
from zope import schema
from ntpu.content.article import IArticle
from zope.interface import Interface
from ntpu.content import MessageFactory as _


class RetractArticle(form.SchemaForm):
    grok.name('set_password')
    grok.require('cmf.ManagePortal')
    grok.context(Interface)

    # user = api.user.get(username='example@mail.com')
    # user.setSecurityProfile(password='XXXXX')

    """
                'assignExternalReviewer1',
                'invitEmail1',
                'acceptInvit1',
                'acceptOrReject1',
                'externalReviewerComment1',
                'reviewCommentAttached1',
                'reviewConfirm1',
    """

    def set_password(self, email):
        user = api.user.get(username=email)
        user.setSecurityProfile(password='00000')
        return


    def render(self):
        import pdb; pdb.set_trace()
        return
