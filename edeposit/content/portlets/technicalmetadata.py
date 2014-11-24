from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.content import MessageFactory as _

class ITechnicalMetadata(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ITechnicalMetadata)
    def __init__(self):
        pass

    @property
    def title(self):
        return _(u"Technical Metadata")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('technicalmetadata.pt')


class AddForm(base.AddForm):
    form_fields = form.Fields(ITechnicalMetadata)

    def create(self, data):
        return Assignment(**data)

