from five import grok
from zope.interface import Interface
from ntpu.content.article import IArticle
from plone import api
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from ntpu.content import MessageFactory as _


#check have attach file
@grok.subscribe(IArticle, IBeforeTransitionEvent)
def checkAttachFile(item, event):
#    import pdb; pdb.set_trace()
    if event.new_state.getId() != 'submitted':
        return

    if not item.getChildNodes():
        message = _(u"Must be upload Attach file.")

        api.portal.show_message(
            message=message,
            request=item.REQUEST,
            type='error'
        )
        raise Invalid(message)

    return


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def checkCommentReply(item, event):
    if event.new_state.getId() != 'retria':
        return

    if item.commentReply is not None:
        return

    message = _(u"Must be upload comment replay file.")
    api.portal.show_message(
        message=message,
        request=item.REQUEST,
        type='error'
    )
    raise Invalid(message)


@grok.subscribe(IArticle, IBeforeTransitionEvent)
def checkReviewFeedback(item, event):
    if event.new_state.getId() != 'modifyThenReview':
        return

    if item.reviewFeedback or item.reviewFeedbackText:
        return

    message = _(u"must be upload review feedback comment file")
    api.portal.show_message(
        message=message,
        request=item.REQUEST,
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
        item.reviewFeedback = None
        item.scoreR1Q1 = None
        item.scoreR1Q2 = None
        item.scoreR1Q3 = None
        item.scoreR1Q4 = None
        item.scoreR2Q1 = None
        item.scoreR2Q2 = None
        item.scoreR2Q3 = None
        item.scoreR2Q4 = None
        item.scoreR3Q1 = None
        item.scoreR3Q2 = None
        item.scoreR3Q3 = None
        item.scoreR3Q4 = None

        item.reindexObject()
