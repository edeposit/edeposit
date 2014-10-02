# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope.interface import invariant, Invalid
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.directives import form
from edeposit.content import MessageFactory as _
from zope import schema
from z3c.form import group, field, button
from edeposit.content.originalfile import IOriginalFile
from five import grok
from plone.z3cform.layout import FormWrapper
from zope.formlib import form as formlib
import edeposit.amqp.aleph
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from zope.lifecycleevent import modified
from plone import api
import sys
from Acquisition import aq_inner, aq_parent

class IISBNGeneration(form.Schema):
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = False,
        )

class ISBNGenerationForm(form.SchemaForm):
    grok.name("isbn-generate")
    grok.require("cmf.ReviewPortalContent")
    grok.context(IOriginalFile)
    schema = IISBNGeneration
    ignoreContext = True
    label = u""
    description = u""

    @button.buttonAndHandler(u'Přiřadit ISBN')
    def handleOK(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        try:
            valid = edeposit.amqp.aleph.isbn.is_valid_isbn(data['isbn'])
        except:
            print sys.exc_info()
            raise ActionExecutionError(Invalid(u"Objevila se nějaká chyby při volání Aleph služby! (%s)" % (str(sys.exc_info()),)))

        if not valid:
            raise ActionExecutionError(Invalid(u"ISBN není validní!"))

        try:
            appearedAtAleph = edeposit.amqp.aleph.aleph.getISBNCount(data['isbn'])
        except:
            print sys.exc_info()
            raise ActionExecutionError(Invalid(u"Objevila se nějaká chyby při volání Aleph služby! (%s)" % (str(sys.exc_info()),)))

        if appearedAtAleph:
            raise ActionExecutionError(Invalid(u"ISBN už v Alephu existuje!"))

        wft = api.portal.get_tool('portal_workflow')
        self.context.isbn = data['isbn']
        modified(self.context)
        wft.doActionFor(self.context, 'submitISBNGeneration')
        self.status = u"Hotovo!"
    pass

class PortletFormView(FormWrapper):
     """ Form view which renders z3c.forms embedded in a portlet.
     Subclass FormWrapper so that we can use custom frame template. """
     index = ViewPageTemplateFile("formwrapper.pt")

class IISBNGeneratingPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    pass

class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('isbngeneratingportlet.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.form_wrapper = self.createForm()

    def createForm(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone 3 view
        """
        context = aq_inner(self.context)
        returnURL = self.context.absolute_url()
        form = ISBNGenerationForm(context, self.request)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context) # Make sure acquisition chain is respected
        view.form_instance = form
        return view

    @property
    def available(self):
        context = aq_inner(self.context)
        return not context.isbn

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IISBNGeneratingPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"ISBN Generating Portlet")



# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = formlib.Fields(IISBNGeneratingPortlet)
    def create(self, data):
        return Assignment(**data)

