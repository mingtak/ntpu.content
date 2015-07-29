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

    def render(self):
        import pdb; pdb.set_trace()
        return
