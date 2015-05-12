from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from plone import api
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from ntpu.content import MessageFactory as _


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def checkCommentReply(item, event):
    if event.new_state.getId() != 'retria':
        return

    if item.commentReply is not None:
        return

    message = _(u"Must be upload comment replay file.")
    api.portal.show_message(
        message=message,
        request=obj.REQUEST,
        type='error'
    )
    raise Invalid(message)


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def checkReviewFeedback(item, event):
    if event.new_state.getId() != 'modifyThenReview':
        return

    if item.reviewFeedback is not None:
        return

    message = _(u"must be upload review feedback comment file")
    api.portal.show_message(
        message=message,
        request=obj.REQUEST,
        type='error'
    )
    raise Invalid(message)


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def retract(item, event):
    if event.new_state.getId() == 'draft':
        item.blindSetup = None
        item.assignInternalReviewer = None
        item.assignExternalReviewer1 = None
        item.invitEmail1 = None
        item.acceptInvit1 = None
        item.acceptOrReject1 = None
        item.externalReviewerComment1 = None
        item.reviewCommentAttached1 = None
        item.reviewConfirm1 = None
        item.assignExternalReviewer2 = None
        item.invitEmail2 = None
        item.acceptInvit2 = None
        item.acceptOrReject2 = None
        item.externalReviewerComment2 = None
        item.reviewCommentAttached2 = None
        item.reviewConfirm2 = None
        item.assignExternalReviewer3 = None
        item.invitEmail3 = None
        item.acceptInvit3 = None
        item.acceptOrReject3 = None
        item.externalReviewerComment3 = None
        item.reviewCommentAttached3 = None
        item.reviewConfirm3 = None
        item.reindexObject()
