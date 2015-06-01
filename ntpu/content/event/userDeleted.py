from five import grok
from plone import api
from Products.PluggableAuthService.interfaces.events import IPrincipalDeletedEvent


@grok.subscribe(IPrincipalDeletedEvent)
def modifiedProfile(event):
    portal = api.portal.get()
    catalog = portal.portal_catalog
    brain = catalog({'Creator':event.object, 'Type':'Profile'})
    for item in brain:
        api.content.delete(obj=item.getObject())
