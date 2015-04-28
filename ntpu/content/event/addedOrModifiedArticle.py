from five import grok
#from zope.interface import Interface
from plone import api
#from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectAddedEvent
from ntpu.content.article import IArticle
from DateTime import DateTime

from ntpu.content import MessageFactory as _


# for Owner
@grok.subscribe(IArticle, IObjectAddedEvent)
@grok.subscribe(IArticle, IObjectModifiedEvent)
def addedOrModifiedArticle(obj, event):

    ownerId = obj.owner_info()['id']
    currentUserId = api.user.get_current().getId()
    if ownerId != currentUserId:
        return

    if api.content.get_state(obj) != 'draft':
        api.portal.show_message(
            message=_(u"Can not modify the contents of the period for review"),
            request=obj.REQUEST,
            type='warning'
        )
        raise
    if obj.attachFile is None:
        return

    attachFile, obj.attachFile = obj.attachFile, None
    with api.env.adopt_roles(['Manager']):
        fileObj = api.content.create(
            container=obj,
            type='File',
            title='AttachFile%s' % DateTime().strftime('%Y%m%d'),
            file=attachFile,
        )
    return
