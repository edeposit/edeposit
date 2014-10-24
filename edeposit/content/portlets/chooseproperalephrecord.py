# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone import api
from zope import schema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility, getUtility

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

from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder
from zope.lifecycleevent import modified
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from Acquisition import aq_inner, aq_parent
from zope.security import checkPermission

class PortletFormView(FormWrapper):
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
             intids = getUtility(IIntIds)
             self.context.related_aleph_record = RelationValue(intids.getId(alephRecord))
             modified(self.context)
             wft = api.portal.get_tool('portal_workflow')
             wft.doActionFor(self.context, 'toAcquisitionPreparing')
             [ ii for ii in range(5) if INextState(self.context).doActionFor() ]
        self.status = u"Hotovo!"


class IChooseProperAlephRecord(IPortletDataProvider):
     pass

class Assignment(base.Assignment):
    implements(IChooseProperAlephRecord)

    def __init__(self):
        pass

    @property
    def title(self):
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

    @property
    def available(self):
         context = aq_inner(self.context)
         return 'chooseProperAlephRecord' in api.content.get_state(context) and checkPermission('cmf.ReviewPortalContent',context)

class AddForm(base.AddForm):
    form_fields = formlib.Fields(IChooseProperAlephRecord)

    def create(self, data):
        return Assignment(**data)
