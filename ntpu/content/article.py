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
from DateTime import DateTime

from ntpu.content.config import CountryList, ArticleLanguage, ArticleType, AcceptOrReject, BlindSetup

from ntpu.content import defaultForms

from ntpu.content import MessageFactory as _


@grok.provider(IContextSourceBinder)
def availableInternalReviewer(context):
    internalReviewers = api.user.get_users(groupname='InternalReviewer')
    terms = []
    for item in internalReviewers:
        terms.append(SimpleVocabulary.createTerm(item.getId(), item.getId(), "%s, %s" %
            (item.getId(), ('' if item.getProperty('fullname') is None else item.getProperty('fullname')))))
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def availableExternalReviewer(context):
    externalReviewers = api.user.get_users(groupname='ExternalReviewer')
    terms = []
    for item in externalReviewers:
        terms.append(SimpleVocabulary.createTerm(item.getId(), item.getId(), "%s, %s" %
            (item.getId(), ('' if item.getProperty('fullname') is None else item.getProperty('fullname')))))
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def availableAuthor(context):
    ownerId = context.owner_info()['id']
    catalog = context.portal_catalog
    brain = catalog({"Type":"Author", "Creator":ownerId})
    terms = []
    for item in brain:
        terms.append(SimpleVocabulary.createTerm(item.UID, item.UID, "%s, %s" %
            (item.authorNameE, ('' if item.authorNameC is None else item.authorNameC))))
    return SimpleVocabulary(terms)


class AlreadySelected(Invalid):
    __doc__ = _(u"This reviewer already selected.")


class IArticle(form.Schema, IImageScaleTraversable):
    """
    Contribute article
    """

    form.fieldset(
        _(u'Review State'),
        label=_(u"Review State"),
        fields=['blindSetup', 'assignInternalReviewer', 'assignExternalReviewer',
                'assignExtraReviewer', 'acceptOrReject', 'externalReviewerComment'],
    )


    dexterity.write_permission(blindSetup='ntpu.content.IsSuperEditor')
    dexterity.read_permission(blindSetup='ntpu.content.IsSuperEditor')
    blindSetup = schema.Choice(
        title=_(u'Blind setup'),
        vocabulary=BlindSetup,
        default=True,
        required=True,
    )

    dexterity.write_permission(assignInternalReviewer='ntpu.content.IsSuperEditor')
    dexterity.read_permission(assignInternalReviewer='ntpu.content.IsSuperEditor')
    assignInternalReviewer = schema.Choice(
        title=_(u'Assign internal reviewer'),
        source=availableInternalReviewer,
        default=None,
        required=True,
    )

    dexterity.write_permission(assignExternalReviewer='ntpu.content.IsInternalReviewer')
    dexterity.read_permission(assignExternalReviewer='ntpu.content.IsInternalReviewer')
    assignExternalReviewer = schema.List(
        title=_(u'Assign external reviewer'),
        value_type=schema.Choice(
            source=availableExternalReviewer,
        ),
        min_length=2,
        max_length=2,
        required=True,
    )

    dexterity.write_permission(assignExtraReviewer='ntpu.content.IsInternalReviewer')
    dexterity.read_permission(assignExtraReviewer='ntpu.content.IsInternalReviewer')
    assignExtraReviewer = schema.Choice(
        title=_(u'Assign external reviewer'),
        source=availableExternalReviewer,
        required=False,
    )

#    form.mode(acceptOrReject='hidden')
    dexterity.write_permission(acceptOrReject='ntpu.content.IsExternalReviewer')
    dexterity.read_permission(acceptOrReject='ntpu.content.IsExternalReviewer')
    acceptOrReject = schema.Choice(
        title=_(u'Accept or Reject'),
        vocabulary=AcceptOrReject,
        default=None,
        required=True,
    )

    dexterity.write_permission(externalReviewerComment='ntpu.content.IsExternalReviewer')
    dexterity.read_permission(externalReviewerComment='ntpu.content.IsExternalReviewer')
    externalReviewerComment = schema.Text(
        title=_(u'External reviewer comment'),
        required=True,
    )

    form.fieldset(
        _(u'manuscript metadata'),
        label=_(u"Manuscript Metadata"),
        fields=['submittingFrom', 'articleLanguage', 'articleType', 'articleTitle', 'engTitle',
                'keywords', 'engKeywords', 'abstract', 'engAbstract', 'coverLetter'],
        description=_(u"Submit a new manuscript(fields in RED DOT are Required)"),
    )

    dexterity.write_permission(submittingFrom='ntpu.content.IsOwner')
    submittingFrom = schema.Choice(
        title=_(u'Submitting from'),
        description=_(u'I am submitting from'),
        vocabulary=CountryList,
        default=_(u"Taiwan"),
        required=True,
    )

    dexterity.write_permission(articleLanguage='ntpu.content.IsOwner')
    articleLanguage = schema.Choice(
        title=_(u'Language'),
        vocabulary=ArticleLanguage,
        default=_(u"zh-tw"),
        required=True,
    )

    dexterity.write_permission(articleType='ntpu.content.IsOwner')
    articleType = schema.Choice(
        title=_(u'Article type'),
        vocabulary=ArticleType,
        default=_(u'Original paper'),
        required=True,
    )

    dexteritytextindexer.searchable('articleTitle')
    dexterity.write_permission(articleTitle='ntpu.content.IsOwner')
    articleTitle = schema.TextLine(
        title=_(u'Article title'),
        required=True,
    )

    dexteritytextindexer.searchable('engTitle')
    dexterity.write_permission(engTitle='ntpu.content.IsOwner')
    engTitle = schema.TextLine(
        title=_(u'English title'),
        required=False,
    )

    dexteritytextindexer.searchable('keywords')
    dexterity.write_permission(keywords='ntpu.content.IsOwner')
    keywords = schema.TextLine(
        title=_(u'Keywords'),
        description=_(u'Maximum 5 keywords, separated with commas.'),
        required=True,
    )

    dexteritytextindexer.searchable('engKeywords')
    dexterity.write_permission(engKeywords='ntpu.content.IsOwner')
    engKeywords = schema.TextLine(
        title=_(u'English keywords'),
        description=_(u'Maximum 5 keywords, separated with commas.'),
        required=False,
    )

    dexteritytextindexer.searchable('abstract')
    dexterity.write_permission(abstract='ntpu.content.IsOwner')
    abstract = schema.Text(
        title=_(u'Abstract'),
        required=True,
    )

    dexteritytextindexer.searchable('engAbstract')
    dexterity.write_permission(engAbstract='ntpu.content.IsOwner')
    engAbstract = schema.Text(
        title=_(u'English abstract'),
        required=False,
    )

    dexteritytextindexer.searchable('coverLetter')
    dexterity.write_permission(coverLetter='ntpu.content.IsOwner')
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
                      default=u"Select authors and order, first is main author,\
                                second is 2'nd author...<br> \
                                Note: Before submitting, you mustbe agree 'All author consent' \
                                , 'Exclusive or non-exclusive license' and check them."),
    )

    dexterity.write_permission(authors='ntpu.content.IsOwner')
    authors = schema.List(
        title=_(u'Authors'),
        description=_(u'Please select authors'),
        value_type=schema.Choice(
            title=_(u'name'),
            source=availableAuthor,
            required=True,
        ),
        min_length=1,
        required=True,
    )

    dexterity.write_permission(corresponging='ntpu.content.IsOwner')
    corresponging = schema.List(
        title=_(u'Corresponding authors'),
        description=_(u'Select at least one corresponding author.'),
        value_type=schema.Choice(
            title=_(u'name'),
            source=availableAuthor,
            required=True,
        ),
        min_length=1,
        required=True,
    )

    dexterity.write_permission(allAuthorConsent='ntpu.content.IsOwner')
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

    dexterity.write_permission(license='ntpu.content.IsOwner')
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

    @invariant
    def validateExtraReviewer(data):
        if data.assignExternalReviewer is None:
            return True
        if data.assignExtraReviewer in data.assignExternalReviewer:
            raise AlreadySelected(_(u"This reviewer already selected."))


class Article(Container):
    grok.implements(IArticle)


class SampleView(dexterity.DisplayForm):
    """ sample view class """

    grok.context(IArticle)
    grok.require('zope2.View')
    grok.name('view')

    def checkIdInReviewerList(self):
        roles = api.user.get_roles()
        context = self.context
        currentUserId = api.user.get_current().getId()
        if len(set(['Manager', 'Site Administrator', 'Super Editor']) & set(roles)) > 0:
            return True
        if len(set(['Internal Reviewer', 'External Reviewer']) & set(roles)) > 0:
            if (context.assignInternalReviewer is not None and currentUserId in context.assignInternalReviewer) or \
               (context.assignExternalReviewer is not None and currentUserId in context.assignExternalReviewer) or \
               (context.assignExtraReviewer is not None and currentUserId in context.assignExtraReviewer):
                return True
        else:
            return False

    def alreadyReview(self):
        roles = api.user.get_roles()
        context = self.context
        currentUserId = api.user.get_current().getId()
        if list(set(['Manager', 'Site Administrator', 'Super Editor']) & set(roles)) != []:
            return False

        alreadyReviewer = []
        if self.getSelfBrain().reviewResults is not None:
            for item in self.getSelfBrain().reviewResults:
                alreadyReviewer.append(item[0])

        if currentUserId in alreadyReviewer:
            return True
        else:
            return False

    def getBlind(self):
        return self.context.blindSetup

    def getRoles(self):
        return api.user.get_roles()

    def isAnonymous(self):
        return api.user.is_anonymous()

    def getCurrent(self):
        return api.user.get_current()

    def isOwner(self):
        if self.isAnonymous():
            return False
        currentUserId = self.getCurrent().getId()
        ownerId = self.context.owner_info()['id']
        if currentUserId == ownerId:
            return True
        else:
            return False

    def getSelfBrain(self):
        catalog = self.context.portal_catalog
        uid = self.context.UID()
        brain = catalog(UID=uid)
        return brain[0]


@indexer(IArticle)
def submittingFrom_indexer(obj):
    return obj.submittingFrom
grok.global_adapter(submittingFrom_indexer, name='submittingFrom')

@indexer(IArticle)
def articleLanguage_indexer(obj):
    return obj.articleLanguage
grok.global_adapter(articleLanguage_indexer, name='articleLanguage')

@indexer(IArticle)
def articleType_indexer(obj):
    return obj.articleType
grok.global_adapter(articleType_indexer, name='articleType')

@indexer(IArticle)
def articleTitle_indexer(obj):
    result = []
    if obj.articleTitle is not None:
        result.append(obj.articleTitle)
    if obj.engTitle is not None:
        result.append(obj.engTitle)
    return result
grok.global_adapter(articleTitle_indexer, name='articleTitle')

@indexer(IArticle)
def articleTitleC_indexer(obj):
    return obj.articleTitle
grok.global_adapter(articleTitleC_indexer, name='articleTitleC')

@indexer(IArticle)
def articleTitleE_indexer(obj):
    return obj.articleTitleE
grok.global_adapter(articleTitleE_indexer, name='articleTitleE')

@indexer(IArticle)
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

@indexer(IArticle)
def keywordsC_indexer(obj):
    return obj.keywords.split(',')
grok.global_adapter(keywordsC_indexer, name='keywordsC')

@indexer(IArticle)
def keywordsE_indexer(obj):
    return obj.engKeywords.split(',')
grok.global_adapter(keywordsE_indexer, name='keywordsE')

@indexer(IArticle)
def blindSetup_indexer(obj):
    return obj.blindSetup
grok.global_adapter(blindSetup_indexer, name='blindSetup')

@indexer(IArticle)
def assignInternalReviewer_indexer(obj):
    return obj.assignInternalReviewer
grok.global_adapter(assignInternalReviewer_indexer, name='assignInternalReviewer')

@indexer(IArticle)
def assignExternalReviewer_indexer(obj):
    return obj.assignExternalReviewer
grok.global_adapter(assignExternalReviewer_indexer, name='assignExternalReviewer')

@indexer(IArticle)
def assignExtraReviewer_indexer(obj):
    return obj.assignExtraReviewer
grok.global_adapter(assignExtraReviewer_indexer, name='assignExtraReviewer')

@indexer(IArticle)
def acceptOrReject_indexer(obj):
    return obj.acceptOrReject
grok.global_adapter(acceptOrReject_indexer, name='acceptOrReject')

@indexer(IArticle)
def reviewResults_indexer(obj):
    catalog = obj.portal_catalog
    catalogItem = catalog({'UID':obj.UID()})
    if len(catalogItem) == 0:
        return
    else:
        catalogItem = catalogItem[0]
    results = catalogItem.reviewResults
    if obj.acceptOrReject is None:
        return results
    if results is None:
        results = []
    currentUserId = api.user.get_current().getId()
    now = DateTime().strftime('%c')
    results.append([currentUserId, now,
                    obj.acceptOrReject,
                    '%s' % obj.externalReviewerComment])
    obj.acceptOrReject = None
    obj.externalReviewerComment = None
    return results
grok.global_adapter(reviewResults_indexer, name='reviewResults')

@indexer(IArticle)
def authorsInformation_indexer(obj):
    catalog = obj.portal_catalog
    selfUID = obj.UID()
    selfBrain = catalog(UID=selfUID)
    if len(selfBrain) > 0:
        selfBrain = selfBrain[0]
        ownerId = obj.owner_info()['id']
        currentUserId = api.user.get_current().getId()
        if ownerId != currentUserId:
            return selfBrain.authorsInformation

    result = []
    for uid in obj.authors:
        brain = catalog(UID=uid)
        if len(brain) == 0:
            continue
        item = brain[0]
        authorInfo = {
            'authorNameC':item.authorNameC,
            'authorNameE':item.authorNameE,
            'institutionC':item.institutionC,
            'institutionE':item.institutionE,
            'titleC':item.titleC,
            'titleE':item.titleE,
            'email':item.email,
            'phone':item.phone,
        }
        result.append(authorInfo)
    return result
grok.global_adapter(authorsInformation_indexer, name='authorsInformation')
