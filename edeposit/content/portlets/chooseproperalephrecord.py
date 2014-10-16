# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements
from itertools import chain
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone import api
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.user import MessageFactory as _

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from plone.z3cform.layout import FormWrapper

from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from zope.lifecycleevent import modified
from five import grok
from plone.directives import form
from zope.formlib import form as formlib
from z3c.form import group, field, button
from z3c.relationfield.schema import RelationChoice, Relation
from edeposit.content.originalfile import IOriginalFile

class PortletFormView(FormWrapper):
     """ Form view which renders z3c.forms embedded in a portlet.
     Subclass FormWrapper so that we can use custom frame template. """
     index = ViewPageTemplateFile("formwrapper.pt")

@grok.provider(IContextSourceBinder)
def availableAlephRecords(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.alephrecord",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

class IChooseProperAlephRecordForm(form.Schema):
    related_aleph_record = RelationChoice( title=u"Odpovídající záznam v Alephu",
                                           required = False,
                                           source = availableAlephRecords)

class ChooseProperAlephRecordForm(form.SchemaForm):
    schema = IChooseProperAlephRecordForm
    ignoreContext = True
    label = u""
    description = u""
    grok.context(IOriginalFile)

    @button.buttonAndHandler(u'Přiřadit')
    def handleOK(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        alephRecord = data.get('related_aleph_record',None)
        if alephRecord:
            self.context.related_aleph_record = RelationValue(intids.getId(alephRecord))
            modified(self.context)
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(self.context, 'toAcquisitionPreparing')
        self.status = u"Hotovo!"


class IChooseProperAlephRecord(IPortletDataProvider):
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

    implements(IChooseProperAlephRecord)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return __(u"Choose proper aleph record")


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('chooseproperalephrecord.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.form_wrapper = self.createForm()

    def createForm(self):
        context = aq_inner(self.context)
        returnURL = self.context.absolute_url()
        form = ChooseProperAlephRecordForm(context, self.request)

        # Wrap a form in Plone view
        view = PortletFormView(context, self.request)
        view = view.__of__(context) # Make sure acquisition chain is respected
        view.form_instance = form
        return view

    # @property
    # def available(self):
    #     # return 'ISBNGeneration' in api.content.get_state(self.context)
    #     context = aq_inner(self.context)
    #     return not context.isbn


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = formlib.Fields(IChooseProperAlephRecord)

    def create(self, data):
        return Assignment(**data)
