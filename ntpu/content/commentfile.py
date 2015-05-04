from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from z3c.relationfield import RelationValue

from plone.formwidget.contenttree import ObjPathSourceBinder
from ntpu.content.profile import IProfile
from plone import api
from ntpu.content.config import AcceptOrReject
from ntpu.content import MessageFactory as _

"""
@grok.provider(IContextSourceBinder)
def ownerProfile(context):
    import pdb; pdb.set_trace()
    return ObjPathSourceBinder(Type="Profile", groups="ExternalReviewer")(context)
"""

class ICommentFile(form.Schema, IImageScaleTraversable):
    """
    Review comment attached file
    """

    reviewer = RelationChoice(
        title=_('Reviewer'),
        source= ObjPathSourceBinder(Type="Profile", groups="ExternalReviewer"),
        required=True,
    )

    acceptOrReject = schema.Choice(
        title=_(u'Result of Review'),
        vocabulary=AcceptOrReject,
        default=None,
        required=False,
    )

    externalReviewerComment = schema.Text(
        title=_(u'External reviewer comment'),
        required=False,
    )

    reviewCommentAttached = NamedBlobFile(
        title=_(u'External reviewer comment attached file'),
        required = False,
    )


class CommentFile(Container):
    grok.implements(ICommentFile)


class SampleView(grok.View):
    """ sample view class """

    grok.context(ICommentFile)
    grok.require('zope2.View')
    # grok.name('view')
    # Add view methods here
