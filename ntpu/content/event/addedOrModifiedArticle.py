# -*- coding: utf-8 -*-
from five import grok
#from zope.interface import Interface
from plone import api
#from Products.PlonePAS.events import UserInitialLoginInEvent, UserLoggedInEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent, IObjectAddedEvent
from ntpu.content.article import IArticle
from DateTime import DateTime
import os
from plone import namedfile

from ntpu.content import MessageFactory as _


@grok.subscribe(IArticle, IObjectModifiedEvent)
def check_interReviewer(obj, event):
    currentUserId = api.user.get_current().getId()
    state = api.content.get_state(obj=obj)
    if state != 'internalAssigned':
        return

    request = obj.REQUEST
    allower = []
    if obj.assignInternalReviewer:
        allower.append(obj.assignInternalReviewer.to_object.owner_info()['id'])
    if obj.assignExternalReviewer1:
        allower.append(obj.assignExternalReviewer1.to_object.owner_info()['id'])
    if obj.assignExternalReviewer2:
        allower.append(obj.assignExternalReviewer2.to_object.owner_info()['id'])
    if obj.assignExternalReviewer3:
        allower.append(obj.assignExternalReviewer3.to_object.owner_info()['id'])
    if currentUserId not in allower and 'Manager' not in api.user.get_roles():
        api.portal.show_message(message=u'身份錯誤，您沒有修改本稿件的權限，請確認您的登入身份，或者您可以聯絡系統管理員.',
            request=request, type='error')
        raise


# for Owner
@grok.subscribe(IArticle, IObjectAddedEvent)
@grok.subscribe(IArticle, IObjectModifiedEvent)
def addedOrModifiedArticle(obj, event):

    ownerId = obj.owner_info()['id']
    currentUserId = api.user.get_current().getId()
    if ownerId != currentUserId and 'Site Administrator' not in api.user.get_roles(username=currentUserId):
        return

    """
    reviewResults = 0
    if obj.acceptOrReject1 is not None:
        reviewResults += 1
    if obj.acceptOrReject2 is not None:
        reviewResults += 1
    if obj.acceptOrReject3 is not None:
        reviewResults += 1
    if reviewResults > 1:
        attachFile, obj.attachFile = obj.attachFile, None
        with api.env.adopt_roles(['Manager']):
            if attachFile is None:
                return
            fileObj = api.content.create(
                container=obj,
                type='File',
                title='AttachFile%s' % DateTime().strftime('%Y%m%d'),
                file=attachFile,
            )
        return
    """

    if (api.content.get_state(obj) not in ['draft', 'modifyThenReview']) and ('Site Administrator' not in api.user.get_roles()):
        api.portal.show_message(
            message=_(u"Can not modify the contents of the period for review"),
            request=obj.REQUEST,
            type='warning'
        )
        raise
    if obj.attachFile is None:
        return

    attachFile, obj.attachFile = obj.attachFile, None
    with api.env.adopt_roles(['Manager']):
        if attachFile is None:
            return
        fileObj = api.content.create(
            container=obj,
            type='File',
            title='AttachFile%s' % DateTime().strftime('%Y%m%d'),
            file=attachFile,
        )

    if fileObj.file.filename[-4:] == u"docx":
        filename = '/tmp/utaipei_temp.docx'
    else:
        filename = '/tmp/utaipei_temp.doc'

    fileObj = fileObj.file.open()
    with open(filename, 'w') as tempFile:
        data = fileObj.read()
        tempFile.write(data)

    os.popen('cd /tmp; lowriter --convert-to pdf %s' % filename)

    with open('/tmp/utaipei_temp.pdf') as tempFile:
        pdfFile = tempFile.read()

    with api.env.adopt_roles(['Manager']):
        pdf_file = api.content.create(
            container=obj,
            type='File',
            title='AttachPdfFile%s' % DateTime().strftime('%Y%m%d'),
            file=namedfile.NamedBlobFile(data=pdfFile, filename=u'AttachPdfFile.pdf')
        )
    return
