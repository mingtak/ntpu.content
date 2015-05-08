from five import grok
from plone import api
from plone.supermodel import model
from plone.directives import form

from z3c.form import button, field
from zope import schema
from ntpu.content.article import IArticle

from ntpu.content import MessageFactory as _


class IRetractArticle(model.Schema):
    retractReason = schema.Text(
        title=_(u'Retract reason'),
        required=False,
    )


class RetractArticle(form.SchemaForm):
    grok.name('retractArticle')
    grok.require('zope2.ViewHistory')
    grok.context(IArticle)

    schema = IRetractArticle
    ignoreContext = True
    description = _(u"Please fill in the retract reasons.")

    def update(self):
        self.label = u'%s: %s' % (_(u"Retract article"), self.context.engTitle)
        super(RetractArticle, self).update()
        return

    @button.buttonAndHandler(_(u'Retract'))
    def handleRetract(self, action):
        context = self.context
        data, errors = self.extractData()
        if data['retractReason'] is None:
            api.portal.show_message(message=_(u'No Reason yet!'), request=context.REQUEST, type='warning')
            redirectUrl = u'%s/@@retractArticle' % context.absolute_url()
            return context.REQUEST.response.redirect(redirectUrl)
        context.retractReason = data['retractReason']
        api.content.transition(obj=context, transition='retract')
        api.portal.show_message(message=_(u'Retract Success.'), request=context.REQUEST, type='info')
        return context.REQUEST.response.redirect(context.absolute_url())
        

    @button.buttonAndHandler(_(u"Cancel"))
    def handleCancel(self, action):
        redirect = self.context.REQUEST.response.redirect
        url = self.context.absolute_url()
        return redirect(url)
