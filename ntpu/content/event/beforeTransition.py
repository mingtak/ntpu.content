from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from plone import api
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from ntpu.content import MessageFactory as _


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def retract(item, event):
    if event.new_state.getId() == 'draft':
        item.blindSetup = None
        item.assignInternalReviewer = None
        item.assignInternalReviewer1 = None
        item.assignInternalReviewer2 = None
        item.assignInternalReviewer3 = None
        item.assignExternalReviewer = None
        item.assignExtraReviewer = None
        item.acceptOrReject = None
        item.externalReviewerComment = None
        item.reindexObject()
