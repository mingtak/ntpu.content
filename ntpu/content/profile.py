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

from ntpu.content.config import GenderOption, CountryList, Degree

from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid

from plone.indexer import indexer
from plone import api

# Back references
from Acquisition import aq_inner
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog

# i18n
from ntpu.content import MessageFactory as _


def back_references(source_object, attribute_name):
    """
    Return back references from source object on specified attribute_name
    """
    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)
    result = []
    for rel in catalog.findRelations(
                   dict(to_id=intids.getId(aq_inner(source_object)),
                   from_attribute=attribute_name)):
        obj = intids.queryObject(rel.from_id)
        if obj is not None and checkPermission('zope2.View', obj):
            result.append(obj)
    return result



def checkEmail(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise Invalid(_(u"Invalid email address."))
    return True


class IProfile(form.Schema, IImageScaleTraversable):
    """
    Personal profile
    """

    form.fieldset(
        _(u'Basic'),
        label=_(u"Basic persional info"),
        fields=['myName', 'gender', 'userTitle'],
        description=_(u"Basic persional infomation (fields in RED DOT are Required)"),
    )

    myName = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Full name, include first name and last name'),
        required=True,
    )

    gender = schema.Choice(
        title=_(u'Gender'),
        vocabulary=GenderOption,
        required=True,
    )

    userTitle = schema.TextLine(
        title=_(u'Title'),
        description=_(u'for eg. Dr, Prof, Mr, Ms...'),
        required=True,
    )

    form.fieldset(
        _(u'Contact'),
        label=_(u"Contact Information"),
        fields=['email', 'alternativeEmail', 'phone', 'fax', 'country', 'zip', 'address'],
        description=_(u"Contact Information (fields in RED DOT are Required)"),
    )

    email = schema.TextLine(
        title=_(u'Email'),
        constraint=checkEmail,
        required=True,
    )

    alternativeEmail = schema.TextLine(
        title=_(u'Alternative Email'),
        constraint=checkEmail,
        required=False,
    )

    phone = schema.TextLine(
        title=_('Phone number'),
        required=True,
    )

    fax = schema.TextLine(
        title=_('Fax number'),
        required=False,
    )

    country = schema.Choice(
        title=_(u'Country'),
        vocabulary=CountryList,
        default=_(u"Taiwan"),
        required=True,
    )

    zip = schema.TextLine(
        title=_(u'Zip'),
        required=False,
    )

    address = schema.Text(
        title=_(u'Address'),
        required=True,
    )

    form.fieldset(
        _(u'Educational & Experience'),
        label=_(u"Educational & Experience"),
        fields=['institution', 'position', 'experience', 'education', 'degree', 'expertise'],
        description=_(u"Educational & Experience (fields in RED DOT are Required)"),
    )

    institution = schema.TextLine(
        title=_(u'Institution'),
        required=True,
    )

    position = schema.TextLine(
        title=_(u'Position'),
        required=False,
    )

    experience = schema.Text(
        title=_(u'Experience'),
        required=False,
    )

    education = schema.Text(
        title=_(u'Education'),
        required=False,
    )

    degree = schema.Choice(
        title=_(u'Degree'),
        vocabulary=Degree,
        default=_(u"Bachelor's degree"),
        required=False,
    )

    expertise = schema.Text(
        title=_(u'Expertise'),
        description=_(u'Research area & Expertise'),
        required=False,
    )


class Profile(Container):
    grok.implements(IProfile)


class SampleView(dexterity.DisplayForm):
    """ sample view class """

    grok.context(IProfile)
    grok.require('zope2.View')
    grok.name('view')

    def internalReviewerBackRef(self):
        return back_references(self.context, 'assignInternalReviewer')

    def externalReviewerBackRef(self):
        externalReviewerList = []
        back1 = back_references(self.context, 'assignExternalReviewer1')
        back2 = back_references(self.context, 'assignExternalReviewer2')
        back3 = back_references(self.context, 'assignExternalReviewer3')
        if bool(back1):
#            externalReviewerList.append(back1[0])
           externalReviewerList += back1
        if bool(back2):
#            externalReviewerList.append(back2[0])
           externalReviewerList += back2
        if bool(back3):
#            externalReviewerList.append(back3[0])
           externalReviewerList += back3
        return externalReviewerList

    def newInReview(self):
        """ New InReview article """
        catalog = self.context.portal_catalog
        brain = catalog(
                    {"Type":"Article", "review_state":"inReview"},
                    sort_on="modified",
                    sort_order="reverse",
                )
        return brain

    def newSubmitted(self):
        """ New submitted article """
        catalog = self.context.portal_catalog
        brain = catalog(
                    {"Type":"Article", "review_state":"submitted"},
                    sort_on="modified",
                    sort_order="reverse",
                )
        return brain

    def internalAssigned(self):
        """ internalAssigned article """
        catalog = self.context.portal_catalog
        brain = catalog(
                    {"Type":"Article",
                     "review_state":"internalAssigned",},
                    sort_on="modified",
                    sort_order="reverse",
                )
        return brain



@indexer(IProfile)
def groups_indexer(obj):
    groups = obj.getOwner().getGroups()
    return groups
grok.global_adapter(groups_indexer, name='groups')
