from five import grok
from plone import api
from zope.interface import Interface
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
#from plone.app.contenttypes.interfaces import IDocument, INewsItem, IEvent
#from plone.app.multilingual.interfaces import ILanguage


#grok.templatedir('views_template')

"""
class GetContentType(grok.View):
    grok.context(Interface)
    grok.name('get_contenttype')

    def render(self):
        return self.context.Type()


class IsOwner(grok.View):
    grok.context(Interface)
    grok.name('is_owner')

    def render(self):
        ownerId = self.context.owner_info()['id']
        currentUserId = api.user.get_current().getId()
        return ownerId == currentUserId


class GetRoles(grok.View):
    grok.context(Interface)
    grok.name('get_roles')

    def render(self):
        return api.user.get_roles()


"""
