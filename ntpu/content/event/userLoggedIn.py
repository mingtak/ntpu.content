from five import grok
from zope.interface import Interface
from plone import api
from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent


@grok.subscribe(UserLoggedInEvent)
def userLoggedIn(event):
    catalog = api.portal.get_tool(name='portal_catalog')
    currentUserId = api.user.get_current().getId()
    profile = catalog({'Creator':currentUserId, 'Type':'Profile'})
    if len(profile) == 0:
        return
    profile = profile[0].getObject()
    profile.reindexObject()
