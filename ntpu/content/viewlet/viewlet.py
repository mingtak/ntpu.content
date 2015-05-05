from five import grok
from plone.app.layout.viewlets.interfaces import IBelowContentBody, IBelowContent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ntpu.content.article import IArticle
from ntpu.content.profile import IProfile


#grok.templatedir('template')
"""
  viewlet named rule: Function_ViewletManager_ContextInterface
"""

class Blind_IBelowContentBody_IArticle(grok.Viewlet):
    grok.viewletmanager(IBelowContentBody)
    grok.context(IArticle)
    template = ViewPageTemplateFile('template/blind.pt')

    def render(self):
        return self.template()


class AdminDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/adminDesktop.pt')

    def render(self):
        return self.template()


class SuperEditorDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/superEditorDesktop.pt')

    def render(self):
        return self.template()


class InternalReviewerDesktop_IBelowContent_IProfile(grok.Viewlet):
    grok.viewletmanager(IBelowContent)
    grok.context(IProfile)
    template = ViewPageTemplateFile('template/internalReviewerDesktop.pt')

    def render(self):
        return self.template()

