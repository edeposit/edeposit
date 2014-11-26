from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone import api
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from string import Template
from edeposit.content import MessageFactory as _
from functools import partial
from Acquisition import aq_parent, aq_inner

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
        return _(u"OriginalFiles Links")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('originalfileslinks.pt')

    @property
    def originalfileslinks(self):
        context = self.context.portal_type == 'edeposit.content.originalfile' and aq_parent(aq_inner(self.context)) or self.context
        def linkFactory(of, plone_utils=None):
            type_class = 'contenttype-edeposit.content.originalfile'
            state_class = 'state-' + plone_utils.normalizeString(api.content.get_state(of))
            url = of.absolute_url()
            cls=" ".join([type_class, state_class]).replace(".","-")
            result = dict(content=of.title, cls=cls, href=url)
            return result

        originalFiles = context.listFolderContents(contentFilter={"portal_type" : "edeposit.content.originalfile"})
        links = map(partial(linkFactory,plone_utils=api.portal.get_tool('plone_utils')), 
                    originalFiles)
        return links
                                                
class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IOriginalFilesLinks)

    def create(self, data):
        return Assignment(**data)


