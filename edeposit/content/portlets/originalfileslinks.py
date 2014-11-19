from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.content import MessageFactory as _

class IOriginalFilesLinks(IPortletDataProvider):
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

    implements(IOriginalFilesLinks)
    def __init__(self):
        pass

    @property
    def title(self):
        return __(u"OriginalFiles Links")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('originalfileslinks.pt')

    @property
    def originalfiles(self):
        context = self.context
        originalFiles = context.listFolderContents(contentFilter={"portal_type" : "edeposit.content.originalfile"})
        return originalFiles
                                                
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IOriginalFilesLinks)

    def create(self, data):
        return Assignment(**data)


