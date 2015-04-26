from five import grok
from zope.interface import Interface
from plone import api
#from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from ntpu.content.profile import IProfile
from Products.CMFPlone import utils


@grok.subscribe(IProfile, IObjectModifiedEvent)
def modifiedProfile(obj, event):
#    import pdb; pdb.set_trace()
    owner = api.user.get(username=obj.getOwner().getUserName())
    obj.title = obj.myName
    owner.setMemberProperties(
        mapping={
            "fullname":obj.myName,
            "email":obj.email
        }
    )
    obj.reindexObject()
    utils.set_own_login_name(owner, obj.email)
