from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid, Interface
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

from plone import api
from collective import dexteritytextindexer
from plone.indexer import indexer

from ntpu.content.config import CountryList, ArticleLanguage, ArticleType

from ntpu.content import MessageFactory as _


@grok.provider(IContextSourceBinder)
def availableAuthor(context):
    current_user = api.user.get_current().id
    catalog = context.portal_catalog
    brain = catalog({"Type":"Author", "Creator":current_user})
    terms = []
    for item in brain:
        terms.append(SimpleVocabulary.createTerm(item.UID, item.UID, "%s, %s" %
            (item.authorNameE, ('' if item.authorNameC is None else item.authorNameC))))
    return SimpleVocabulary(terms)


class IArticle(form.Schema, IImageScaleTraversable):
    """
    Contribute article
    """
    form.fieldset(
        _(u'manuscript metadata'),
        label=_(u"Manuscript Metadata"),
        fields=['submittingFrom', 'articleLanguage', 'articleType', 'articleTitle', 'engTitle',
                'keywords', 'engKeywords', 'abstract', 'engAbstract', 'coverLetter'],
        description=_(u"Submit a new manuscript(fields in RED DOT are Required)"),
    )

    submittingFrom = schema.Choice(
        title=_(u'Submitting from'),
        description=_(u'I am submitting from'),
        values=CountryList,
        default=_(u"Taiwan"),
        required=True,
    )

    articleLanguage = schema.Choice(
        title=_(u'Langeuage'),
        values=ArticleLanguage,
        default=_(u"zh-tw"),
        required=True,
    )

    articleType = schema.Choice(
        title=_(u'Article type'),
        values=ArticleType,
        default=_(u'Original paper'),
        required=True,
    )

    dexteritytextindexer.searchable('articleTitle')
    articleTitle = schema.TextLine(
        title=_(u'Article title'),
        required=True,
    )

    dexteritytextindexer.searchable('engTitle')
    engTitle = schema.TextLine(
        title=_(u'English title'),
        required=False,
    )

    dexteritytextindexer.searchable('keywords')
    keywords = schema.TextLine(
        title=_(u'Keywords'),
        description=_(u'Maximum 5 keywords, separated with commas.'),
        required=True,
    )

    dexteritytextindexer.searchable('engKeywords')
    engKeywords = schema.TextLine(
        title=_(u'English keywords'),
        description=_(u'Maximum 5 keywords, separated with commas.'),
        required=False,
    )

    dexteritytextindexer.searchable('abstract')
    abstract = schema.Text(
        title=_(u'Abstract'),
        required=True,
    )

    dexteritytextindexer.searchable('engAbstract')
    engAbstract = schema.Text(
        title=_(u'English abstract'),
        required=False,
    )

    dexteritytextindexer.searchable('coverLetter')
    coverLetter = schema.Text(
        title=_(u'Cover letter'),
        description=_(u'help_coverLetter',
            default=u'Enter your cover letter here. \
                      DO NOT include your cover letter \
                      in the manuscript file that you \
                      will upload.The word limit of this \
                      column is 1024 characters.'),
        max_length=1024,
        required=False,
    )

    form.fieldset(
        _(u'Authors'),
        label=_(u"Authors"),
        fields=['authors', 'corresponging', 'allAuthorConsent', 'license'],
        description=_(u"help_authors",
                      default=u"Select authors and order, first is main author, second is 2'nd author..."),
    )

    authors = schema.List(
        title=_(u'Authors'),
        description=_(u'Please select authors'),
        value_type=schema.Choice(
            title=_(u'name'),
            source=availableAuthor,
        ),
        required=True,
    )

    corresponging = schema.List(
        title=_(u'Corresponding authors'),
        description=_(u'Select at least one corresponding author.'),
        value_type=schema.Choice(
            title=_(u'name'),
            source=availableAuthor,
        ),
        required=True,
    )

    allAuthorConsent = schema.Bool(
        title=_(u'All author consent'),
        description=_(u'help_allAuthorConsent',
                      default='I confirm this manuscript has not been accepted \
                          for publication elsewhere, is not being considered \
                          for publication elsewhere and does not duplicate material \
                          already published. I confirm all authors consent to \
                          publication of this manuscript.'),
        default=False,
        required=True,
    )

    license = schema.Bool(
        title=_(u'Exclusive or non-exclusive license'),
        description=_(u'help_license', 
                      default='I have read and agreed with the following statements: \
                          1. I am authorized by all co-author(s) to submit this article \
                          on their behalf and as the contact for the Editorial process. \
                          I am responsible for communicating with the other authors about \
                          progress, submissions of revisions and final approval of proofs. \
                          2. All authors agree with the Personal Information Collection \
                          Statement , and the staff of the journal will be using the \
                          personal information that I provided in the APSERS system for \
                          the sole purpose of contacting me concerning the publishing of \
                          the Article. \
                          3. The article I have submitted to the journal for review is \
                          original, has been written by the stated authors and has not been \
                          published elsewhere. Also, the Article is not currently being \
                          considered for publication by any other journal and will not be \
                          submitted for such review while under review by this journal.'),
        default=False,
        required=True,
    )


class Article(Container):
    grok.implements(IArticle)


class SampleView(grok.View):
    """ sample view class """

    grok.context(IArticle)
    grok.require('zope2.View')
    # grok.name('view')


@indexer(Interface)
def submittingFrom_indexer(obj):
    return obj.submittingFrom
grok.global_adapter(submittingFrom_indexer, name='submittingFrom')

@indexer(Interface)
def articleLanguage_indexer(obj):
    return obj.articleLanguage
grok.global_adapter(articleLanguage_indexer, name='articleLanguage')

@indexer(Interface)
def articleType_indexer(obj):
    return obj.articleType
grok.global_adapter(articleType_indexer, name='articleType')

@indexer(Interface)
def articleTitle_indexer(obj):
    result = []
    if obj.articleTitle is not None:
        result.append(obj.articleTitle)
    if obj.engTitle is not None:
        result.append(obj.engTitle)
    return result
grok.global_adapter(articleTitle_indexer, name='articleTitle')

@indexer(Interface)
def articleTitleC_indexer(obj):
    return obj.articleTitle
grok.global_adapter(articleTitleC_indexer, name='articleTitleC')

@indexer(Interface)
def articleTitleE_indexer(obj):
    return obj.articleTitleE
grok.global_adapter(articleTitleE_indexer, name='articleTitleE')

@indexer(Interface)
def keywords_indexer(obj):
    result = []
    if obj.keywords is not None:
        keywords = obj.keywords.split(',')
        for word in keywords:
            result.append(word.strip())
    if obj.engKeywords is not None:
        keywords = obj.engKeywords.split(',')
        for word in keywords:
            result.append(word.strip())
    return result
grok.global_adapter(keywords_indexer, name='keywords')

@indexer(Interface)
def keywordsC_indexer(obj):
    return obj.keywords.split(',')
grok.global_adapter(keywordsC_indexer, name='keywordsC')

@indexer(Interface)
def keywordsE_indexer(obj):
    return obj.engKeywords.split(',')
grok.global_adapter(keywordsE_indexer, name='keywordsE')
