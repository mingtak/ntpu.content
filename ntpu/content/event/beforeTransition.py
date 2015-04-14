from five import grok
from zope.interface import Interface
from plone import api
from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent

@grok.subscribe(UserInitialLoginInEvent)
def userLoggedIn(event):
    catalog = api.portal.get_tool(name='portal_catalog')
    portal = api.portal.get()
    currentUserId = api.user.get_current().getId()
    with api.env.adopt_roles(['Manager']):
        profile = api.content.create(container=portal['members'],
            type='ntpu.content.profile', id=currentUserId, title='Welcome to University of Taipei')
