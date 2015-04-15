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
from plone.formwidget.contenttree import ObjPathSourceBinder

from ntpu.content.config import CountryList, ArticleLanguage, ArticleType, AcceptOrReject, BlindSetup

from ntpu.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IJournal(form.Schema, IImageScaleTraversable):
    """
    Journal content type
    """

    authors = schema.TextLine(
        title=_('Authors'),
        required=True,
    )

    doi = schema.URI(
        title=_('DOI'),
        required=False,
    )

    articleLanguage = schema.Choice(
        title=_(u'Language'),
        vocabulary=ArticleLanguage,
        default=_(u"zh-tw"),
        required=True,
    )

    engTitle = schema.TextLine(
        title=_(u'English title'),
        required=False,
    )

    abstract = schema.Text(
        title=_(u'Abstract'),
        required=True,
    )

    engAbstract = schema.Text(
        title=_(u'English abstract'),
        required=False,
    )

    keywords = schema.TextLine(
        title=_(u'Keywords'),
        required=True,
    )

    engKeywords = schema.TextLine(
        title=_(u'English keywords'),
        required=False,
    )

    attachFile = NamedBlobFile(
        title=_(u'Attach file'),
        required=False,
    )


class Journal(Container):
    grok.implements(IJournal)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IJournal)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
