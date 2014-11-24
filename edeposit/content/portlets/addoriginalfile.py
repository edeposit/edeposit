# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements
from five import grok
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone import api
from zope import schema
from z3c.form import group, field, button
from plone.z3cform.layout import FormWrapper
from zope.formlib import form as formlib
from plone.directives import form
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent

from edeposit.content.epublication import IePublication

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.content import MessageFactory as _
from Acquisition import aq_inner, aq_parent
from zope.security import checkPermission
import sys
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from zope.lifecycleevent import modified
from zope.interface import invariant, Invalid
import edeposit.amqp.aleph

def urlCodeIsValid(value):
    return True

class IOriginalFile(form.Schema):
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = False,
        )

    file = NamedBlobFile(
        title=_(u"Original File of an ePublication"),
        required = False,
        )

    generated_isbn = schema.Bool(
        title = _(u'Generate ISBN'),
        description = _(u'Whether ISBN agency should generate ISBN number.'),
        required = False,
        default = False,
        missing_value = False,
    )

    url = schema.ASCIILine(
        title=_("URL"),
        constraint=urlCodeIsValid,
        required = False,
        )


class AddOriginalFileForm(form.SchemaForm):
    grok.name("add-originalfile")
    grok.require("cmf.AddPortalContent")
    grok.context(IePublication)
    schema = IOriginalFile
    ignoreContext = True
    label = u""
    description = u""

    @button.buttonAndHandler(u'Uložit')
    def handleOK(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if not data['isbn'] and not data['generated_isbn']:
            raise ActionExecutionError(Invalid(u"Je potřeba vyplnit ISBN, nebo zvolit jeho přiřazení."))
            
        try:
            valid = edeposit.amqp.aleph.isbn.is_valid_isbn(data['isbn'] or "")
        except:
            print sys.exc_info()
            raise ActionExecutionError(Invalid(u"Objevila se nějaká chyby při volání Aleph služby! (%s)" % (str(sys.exc_info()),)))

        if data['isbn'] and not valid:
            raise ActionExecutionError(Invalid(u"ISBN není validní!"))

        try:
            appearedAtAleph = data['isbn'] and edeposit.amqp.aleph.aleph.getISBNCount(data['isbn'])
        except:
            print sys.exc_info()
            raise ActionExecutionError(Invalid(u"Objevila se nějaká chyby při volání Aleph služby! (%s)" % (str(sys.exc_info()),)))

        if appearedAtAleph:
            raise ActionExecutionError(Invalid(u"ISBN už v Alephu existuje!"))

        newOriginalFile = createContentInContainer(self.context,
                                                   'edeposit.content.originalfile',
                                                   **data)
        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor(newOriginalFile, 
                        (newOriginalFile.isbn and 'submitDeclarationToISBNValidation')
                        or (newOriginalFile.file and 'submitDeclarationToAntivirus')
                            or 'submitDeclarationToISBNGenerating',
                        comment='handled automatically')
        modified(self.context)
        self.status = u"Hotovo!"
    pass

class PortletFormView(FormWrapper):
     """ Form view which renders z3c.forms embedded in a portlet.
     Subclass FormWrapper so that we can use custom frame template. """
     index = ViewPageTemplateFile("formwrapper.pt")


class IAddOriginalFile(IPortletDataProvider):
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

    implements(IAddOriginalFile)
    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Add OriginalFile")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('addoriginalfile.pt')
    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.form_wrapper = self.createForm()

    def createForm(self):
        """ Create a form instance.

        @return: z3c.form wrapped for Plone 3 view
        """
        context = aq_inner(self.context)
        returnURL = self.context.absolute_url()
        form = AddOriginalFileForm(context, self.request)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context) # Make sure acquisition chain is respected
        view.form_instance = form
        return view

    # @property
    # def available(self):
    #     context = aq_inner(self.context)
    #     return 'Processing' in api.content.get_state(context) \
    #         and checkPermission('cmf.AddPortalContent',context)

# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = formlib.Fields(IAddOriginalFile)

    def create(self, data):
        return Assignment(**data)

