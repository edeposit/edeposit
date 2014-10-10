from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.content import MessageFactory as _

class IOriginalFileExternalLinks(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

class Assignment(base.Assignment):
    implements(IOriginalFileExternalLinks)

    def __init__(self):
        pass

    @property
    def title(self):
        return _(u"Original File External Links")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('originalfileexternallinks.pt')


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IOriginalFileExternalLinks)

    def create(self, data):
        return Assignment(**data)


