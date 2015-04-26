from five import grok
from zope.interface import Interface
from plone import api
from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
import random
import string


@grok.subscribe(UserInitialLoginInEvent)
def userLoggedIn(event):
    catalog = api.portal.get_tool(name='portal_catalog')
    portal = api.portal.get()
    currentUser = api.user.get_current()
    currentUserFullName = currentUser.getProperty('fullname')
    currentUserEmail = currentUser.getProperty('email')
#    currentUserId = currentUser.getId()
#    import pdb; pdb.set_trace()
    profileId = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

    with api.env.adopt_roles(['Manager']):
        profile = api.content.create(container=portal['members'],
            type='ntpu.content.profile',
            id=profileId,
            title=currentUserFullName,
            myName=currentUserFullName,
            email=currentUserEmail,
        )
