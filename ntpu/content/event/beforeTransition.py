from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from plone import api
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from ntpu.content import MessageFactory as _

"""
@grok.subscribe(IArticle, IBeforeTransitionEvent)
def userLoggedIn(item, event):
    if event.transition.getId() != 'submitting':
        return

    import pdb; pdb.set_trace()

    if item.allAuthorConsent == False:
        api.portal.show_message(message=_(u"Please check 'All author consent' field"), request=item.REQUEST, type='warn')
    if item.license == False:
        api.portal.show_message(message=_(u"Please check 'Exclusive or non-exclusive license' field"), request=item.REQUEST, type='warn')

"""
