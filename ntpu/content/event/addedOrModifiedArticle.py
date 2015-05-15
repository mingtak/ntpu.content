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

    """
    reviewResults = 0
    if obj.acceptOrReject1 is not None:
        reviewResults += 1
    if obj.acceptOrReject2 is not None:
        reviewResults += 1
    if obj.acceptOrReject3 is not None:
        reviewResults += 1
    if reviewResults > 1:
        attachFile, obj.attachFile = obj.attachFile, None
        with api.env.adopt_roles(['Manager']):
#            import pdb; pdb.set_trace()
            if attachFile is None:
                return
            fileObj = api.content.create(
                container=obj,
                type='File',
                title='AttachFile%s' % DateTime().strftime('%Y%m%d'),
                file=attachFile,
            )
        return
    """

    if api.content.get_state(obj) not in ['draft', 'modifyThenReview']:
        api.portal.show_message(
            message=_(u"Can not modify the contents of the period for review"),
            request=obj.REQUEST,
            type='warning'
        )
#        import pdb; pdb.set_trace()
        raise
    if obj.attachFile is None:
        return

    attachFile, obj.attachFile = obj.attachFile, None
    with api.env.adopt_roles(['Manager']):
        if attachFile is None:
            return
        fileObj = api.content.create(
            container=obj,
            type='File',
            title='AttachFile%s' % DateTime().strftime('%Y%m%d'),
            file=attachFile,
        )
    return
