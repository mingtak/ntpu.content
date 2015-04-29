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

from ntpu.content.config import CountryList, ArticleLanguage, ArticleType, AcceptOrReject, BlindSetup, Category
from ntpu.content import defaultForms
from ntpu.content.profile import IProfile

from plone.autoform import directives
from plone.formwidget.autocomplete import AutocompleteFieldWidget

from ntpu.content import MessageFactory as _


@grok.provider(IContextSourceBinder)
def availableInternalReviewer(context):
    return ObjPathSourceBinder(Type="Profile", groups="InternalReviewer")(context)


@grok.provider(IContextSourceBinder)
def availableExternalReviewer(context):
    return ObjPathSourceBinder(Type="Profile", groups="ExternalReviewer")(context)


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


class ExternalReviewerNoSelected(Invalid):
    __doc__ = _(u"External reviewer still have no select.")


class ExternalReviewerAlreadySelected(Invalid):
    __doc__ = _(u"External reviewer already selected.")


class IArticle(form.Schema, IImageScaleTraversable):
    """
    Contribute article
    """

    form.fieldset(
        _(u'Review State'),
        label=_(u"Review State"),
        fields=['blindSetup',
                'assignInternalReviewer',
                'assignExternalReviewer1',
                'invitEmail1',
                'acceptInvit1',
                'acceptOrReject1',
                'externalReviewerComment1',
                'reviewCommentAttached1',
                'assignExternalReviewer2',
                'invitEmail2',
                'acceptInvit2',
                'acceptOrReject2',
                'externalReviewerComment2',
                'reviewCommentAttached2',
                'assignExternalReviewer3',
                'invitEmail3',
                'acceptInvit3',
                'acceptOrReject3',
                'externalReviewerComment3',
                'reviewCommentAttached3'],
    )


    dexterity.write_permission(blindSetup='ntpu.content.IsSuperEditor')
    dexterity.read_permission(blindSetup='ntpu.content.IsSuperEditor')
    blindSetup = schema.Choice(
        title=_(u'Blind setup'),
        description=_(u'Recommend using double-blind review'),
        vocabulary=BlindSetup,
        default=True,
        required=True,
    )

    dexterity.write_permission(assignInternalReviewer='ntpu.content.IsSuperEditor')
    dexterity.read_permission(assignInternalReviewer='ntpu.content.IsSuperEditor')
    form.widget(assignInternalReviewer=AutocompleteFieldWidget)
    assignInternalReviewer = RelationChoice(
        title=_(u'Assign internal reviewer'),
        source=availableInternalReviewer,
        default=None,
        required=True,
    )

#### external reviewer 1
    dexterity.write_permission(assignExternalReviewer1='ntpu.content.IsInternalReviewer')
    dexterity.read_permission(assignExternalReviewer1='ntpu.content.IsInternalReviewer')
    form.widget(assignExternalReviewer1=AutocompleteFieldWidget)
    assignExternalReviewer1 = RelationChoice(
        title=_(u'Assign first external reviewer'),
        source=availableExternalReviewer,
        required=False,
    )

    dexterity.write_permission(invitEmail1='ntpu.content.IsInternalReviewer')
    form.mode(invitEmail1='hidden')
    invitEmail1 = schema.TextLine(
        title=_(u'Invit email'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptInvit1='ntpu.content.IsExternalReviewer')
    form.mode(acceptInvit1='hidden')
    acceptInvit1 = schema.Bool(
        title=_(u'Accept invitation'),
        description=_(u'Accept the invitation to review'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptOrReject1='ntpu.content.IsExternalReviewer')
    acceptOrReject1 = schema.Choice(
        title=_(u'Result of Review'),
        vocabulary=AcceptOrReject,
        default=None,
        required=False,
    )

    dexterity.write_permission(externalReviewerComment1='ntpu.content.IsExternalReviewer')
    externalReviewerComment1 = schema.Text(
        title=_(u'External reviewer comment'),
        required=False,
    )

    dexterity.write_permission(reviewCommentAttached1='ntpu.content.IsExternalReviewer')
    reviewCommentAttached1 = NamedBlobFile(
        title=_(u'External reviewer comment attached file'),
        required = False,
    )



#### external reviewer 2
    dexterity.write_permission(assignExternalReviewer2='ntpu.content.IsInternalReviewer')
    dexterity.read_permission(assignExternalReviewer2='ntpu.content.IsInternalReviewer')
    form.widget(assignExternalReviewer2=AutocompleteFieldWidget)
    assignExternalReviewer2 = RelationChoice(
        title=_(u'Assign second external reviewer'),
        source=availableExternalReviewer,
        required=False,
    )

    dexterity.write_permission(invitEmail2='ntpu.content.IsInternalReviewer')
    form.mode(invitEmail2='hidden')
    invitEmail2 = schema.TextLine(
        title=_(u'Invit email'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptInvit2='ntpu.content.IsExternalReviewer')
    form.mode(acceptInvit2='hidden')
    acceptInvit2 = schema.Bool(
        title=_(u'Accept invitation'),
        description=_(u'Accept the invitation to review'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptOrReject2='ntpu.content.IsExternalReviewer')
    acceptOrReject2 = schema.Choice(
        title=_(u'Result of Review'),
        vocabulary=AcceptOrReject,
        default=None,
        required=False,
    )

    dexterity.write_permission(externalReviewerComment2='ntpu.content.IsExternalReviewer')
    externalReviewerComment2 = schema.Text(
        title=_(u'External reviewer comment'),
        required=False,
    )

    dexterity.write_permission(reviewCommentAttached2='ntpu.content.IsExternalReviewer')
    reviewCommentAttached2 = NamedBlobFile(
        title=_(u'External reviewer comment attached file'),
        required = False,
    )


#### external reviewer 3
    dexterity.write_permission(assignExternalReviewer3='ntpu.content.IsInternalReviewer')
    dexterity.read_permission(assignExternalReviewer3='ntpu.content.IsInternalReviewer')
    form.widget(assignExternalReviewer3=AutocompleteFieldWidget)
    assignExternalReviewer3 = RelationChoice(
        title=_(u'Assign third external reviewer'),
        source=availableExternalReviewer,
        required=False,
    )

    dexterity.write_permission(invitEmail3='ntpu.content.IsInternalReviewer')
    form.mode(invitEmail3='hidden')
    invitEmail3 = schema.TextLine(
        title=_(u'Invit email'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptInvit3='ntpu.content.IsExternalReviewer')
    form.mode(acceptInvit3='hidden')
    acceptInvit3 = schema.Bool(
        title=_(u'Accept invitation'),
        description=_(u'Accept the invitation to review'),
        default=None,
        required=False,
    )

    dexterity.write_permission(acceptOrReject3='ntpu.content.IsExternalReviewer')
    acceptOrReject3 = schema.Choice(
        title=_(u'Result of Review'),
        vocabulary=AcceptOrReject,
        default=None,
        required=False,
    )

    dexterity.write_permission(externalReviewerComment3='ntpu.content.IsExternalReviewer')
    externalReviewerComment3 = schema.Text(
        title=_(u'External reviewer comment'),
        required=False,
    )

    dexterity.write_permission(reviewCommentAttached3='ntpu.content.IsExternalReviewer')
    reviewCommentAttached3 = NamedBlobFile(
        title=_(u'External reviewer comment attached file'),
        required = False,
    )

    form.fieldset(
        _(u'manuscript metadata'),
        label=_(u"Manuscript Metadata"),
        fields=['submittingFrom', 'articleLanguage', 'articleType', 'articleTitle', 'engTitle',
                'runningTitle', 'keywords', 'engKeywords', 'abstract', 'engAbstract', 'category', 'coverLetter'],
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

    dexterity.write_permission(runningTitle='ntpu.content.IsOwner')
    runningTitle = schema.TextLine(
        title=_(u'Running title'),
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
        description=_(u'Please limit the number of words in 500 words or less'),
        required=True,
    )

    dexteritytextindexer.searchable('engAbstract')
    dexterity.write_permission(engAbstract='ntpu.content.IsOwner')
    engAbstract = schema.Text(
        title=_(u'English abstract'),
        required=False,
    )

    dexterity.write_permission(category='ntpu.content.IsOwner')
    category = schema.Choice(
        title=_(u'Category'),
        vocabulary=Category,
        default=None,
        required=True,
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

    form.fieldset(
        _(u'Manuscript file'),
        label=_(u"Manuscript file"),
        fields=['modifySubmission'],
        description=_(u'Please upload Manuscript file, and you can upload images after submitting.'),
    )

    dexterity.write_permission(modifySubmission='ntpu.content.IsOwner')
    form.mode(modifySubmission='hidden')
    modifySubmission = NamedBlobFile(
        title=_(u'Modify submission'),
        required=False
    )



    @invariant
    def validateExternalReviewer(data):
        if data.assignExternalReviewer1 == data.assignExternalReviewer2 and data.assignExternalReviewer1 is not None:
            raise Invalid(_(u"This External reviewer already selected."))
        if data.assignExternalReviewer2 == data.assignExternalReviewer3 and data.assignExternalReviewer2 is not None:
            raise Invalid(_(u"This External reviewer already selected."))
        if data.assignExternalReviewer1 == data.assignExternalReviewer3 and data.assignExternalReviewer1 is not None:
            raise Invalid(_(u"This External reviewer already selected."))


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
            if context.assignInternalReviewer is not None:
                if currentUserId == context.assignInternalReviewer.to_object.owner_info()['id']:
                    return True
                if currentUserId == context.assignExternalReviewer1.to_object.owner_info()['id']:
                    return True
                if currentUserId == context.assignExternalReviewer2.to_object.owner_info()['id']:
                    return True
                if currentUserId == context.assignExternalReviewer3.to_object.owner_info()['id']:
                    return True
            else:
                return False
        else:
            return False


#### waiting for modify
    """
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
    """

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
        if len(brain) == 0:
            return brain
        return brain[0]

    def getPhysicalPath(self):
        context = self.context
        pathList = context.getPhysicalPath()
        physicalPath = '/'
        for item in pathList:
            if item == '':
                continue
            physicalPath += '%s/' % item
        return physicalPath


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
    return obj.engTitle
grok.global_adapter(articleTitleE_indexer, name='articleTitleE')

@indexer(IArticle)
def abstract_indexer(obj):
    return obj.abstract
grok.global_adapter(abstract_indexer, name='abstract')

@indexer(IArticle)
def engAbstract_indexer(obj):
    return obj.engAbstract
grok.global_adapter(engAbstract_indexer, name='engAbstract')

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
def category_indexer(obj):
    category = Category.by_value
    return {category[obj.category].value:category[obj.category].title}
grok.global_adapter(category_indexer, name='category')

@indexer(IArticle)
def blindSetup_indexer(obj):
    return obj.blindSetup
grok.global_adapter(blindSetup_indexer, name='blindSetup')

@indexer(IArticle)
def assignInternalReviewer_indexer(obj):
    if obj.assignInternalReviewer is None:
        return
    else:
        return obj.assignInternalReviewer.to_object.getId()
grok.global_adapter(assignInternalReviewer_indexer, name='assignInternalReviewer')

@indexer(IArticle)
def assignExternalReviewer1_indexer(obj):
    result = []
    if obj.assignExternalReviewer1 is None:
        return
    else:
        return obj.assignExternalReviewer1.to_object.getId()
grok.global_adapter(assignExternalReviewer1_indexer, name='assignExternalReviewer1')

@indexer(IArticle)
def invitEmail1_indexer(obj):
    return obj.invitEmail1
grok.global_adapter(invitEmail1_indexer, name='invitEmail1')

@indexer(IArticle)
def acceptInvit1_indexer(obj):
    return obj.acceptInvit1
grok.global_adapter(acceptInvit1_indexer, name='acceptInvit1')

@indexer(IArticle)
def assignExternalReviewer2_indexer(obj):
    result = []
    if obj.assignExternalReviewer2 is None:
        return
    else:
        return obj.assignExternalReviewer2.to_object.getId()
grok.global_adapter(assignExternalReviewer2_indexer, name='assignExternalReviewer2')

@indexer(IArticle)
def invitEmail2_indexer(obj):
    return obj.invitEmail2
grok.global_adapter(invitEmail2_indexer, name='invitEmail2')

@indexer(IArticle)
def acceptInvit2_indexer(obj):
    return obj.acceptInvit2
grok.global_adapter(acceptInvit2_indexer, name='acceptInvit2')

@indexer(IArticle)
def assignExternalReviewer3_indexer(obj):
    result = []
    if obj.assignExternalReviewer3 is None:
        return
    else:
        return obj.assignExternalReviewer3.to_object.getId()
grok.global_adapter(assignExternalReviewer3_indexer, name='assignExternalReviewer3')

@indexer(IArticle)
def invitEmail3_indexer(obj):
    return obj.invitEmail3
grok.global_adapter(invitEmail3_indexer, name='invitEmail3')

@indexer(IArticle)
def acceptInvit3_indexer(obj):
    return obj.acceptInvit3
grok.global_adapter(acceptInvit3_indexer, name='acceptInvit3')

"""
@indexer(IArticle)
def acceptOrReject_indexer(obj):
    return obj.acceptOrReject
grok.global_adapter(acceptOrReject_indexer, name='acceptOrReject')
"""

"""
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
"""

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
