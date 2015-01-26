# -*- coding: utf-8 -*-
from five import grok
import zope
import z3c.form
from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.lifecycleevent import modified
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder, UUIDSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet, INPUT_MODE
import pickle
import os.path
from functools import partial
from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from Products.Five.browser import BrowserView

from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds

from edeposit.content.library import ILibrary
from edeposit.content import MessageFactory as _

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.supermodel import model
from plone.dexterity.utils import getAdditionalSchemata
from Acquisition import aq_inner, aq_base

from zope.component import adapts, createObject
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import Invalid, Interface
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from plone.dexterity.interfaces import IDexterityFTI
from collections import namedtuple
from plone import api
from zope.event import notify
from plone.dexterity.events import AddBegunEvent
from plone.dexterity.events import AddCancelledEvent
from plone.app.discussion.interfaces import IConversation
import operator
import z3c.form.browser.radio

import edeposit.amqp.aleph

from plone.z3cform.layout import wrap_form, FormWrapper

from edeposit.content.epublicationfolder import (
    IePublicationFolder,
)
import z3c.form.browser

from edeposit.content.utils import loadFromAlephByISBN
from edeposit.content.utils import is_valid_isbn
from edeposit.content.utils import getISBNCount

# import edeposit.content.mock
# loadFromAlephByISBN = partial(edeposit.content.mock.loadFromAlephByISBN, num_of_records=1)
# is_valid_isbn = partial(edeposit.content.mock.is_valid_isbn,result=True)
# getISBNCount = partial(edeposit.content.mock.getISBNCount,result=1)

# isbn = "80-85601-24-9" # Karel May : Ahriman Mirza # one record

@grok.provider(IContextSourceBinder)
def records_to_choose_from(context):
    # it takes it from user session
    def getTerm(record):
        id = record.docNumber
        epublication = record.epublication
        authors = [ filter(lambda value: value, [author.title, author.firstName, author.lastName]) \
                    for author in epublication.autori ]
        descAuthors = ",".join(filter(lambda value: value, map(" ".join, authors)))

        keys = ['nazev','podnazev','castDil','nazevCasti','datumVydani','poradiVydani']
        get = partial(getattr,epublication)
        desc = " / ".join(filter(lambda value: value, [get(key,"") for key in keys]))  + " (" + descAuthors + ")"

        return SimpleVocabulary.createTerm(id, id, desc.encode('utf-8'))

    sdm = context.session_data_manager
    session = sdm.getSessionData(create=True)
    aleph_records = session.get('aleph_records')
    if not aleph_records:
        return SimpleVocabulary([])

    terms = map(getTerm, aleph_records)
    return SimpleVocabulary(terms)
    

class ILoadFromSimilar(form.Schema):
    load_isbn = schema.ASCIILine (
        title = u"Předvyplnit formulář podle ISBN",
        required = False,
    )
    form.widget(proper_sysnumber=z3c.form.browser.radio.RadioFieldWidget)
    proper_sysnumber = schema.Choice (
        title = u'Vybraný záznam',
        source = records_to_choose_from,
        required = True
    )

class LoadFromSimilarForm(form.SchemaForm):
    grok.context(IePublicationFolder)
    grok.name('load-from-similar')
    grok.require('edeposit.AddEPublication')

    schema = ILoadFromSimilar
    ignoreContext = True
    prefix = "load-from-similar."

    def updateWidgets(self):
        super(LoadFromSimilarForm,self).updateWidgets()
        if len(self.widgets['proper_sysnumber'].terms) == 0:
            self.widgets['proper_sysnumber'].mode = z3c.form.interfaces.HIDDEN_MODE
            self.widgets['proper_sysnumber'].field.required = False
        else:
            self.widgets['proper_sysnumber'].field.required = True

    @property
    def action(self):
        originalAction = super(LoadFromSimilarForm,self).action
        return os.path.join(os.path.dirname(originalAction),'load-from-similar')

    def getISBN(self,data):
        isbn = data.get('load_isbn',None)
        return isbn

    def extractData(self):
        print "LoadFromSimilarForm - extractData"
        def getErrorView(widget,error):
            view = zope.component.getMultiAdapter( (error, 
                                                    self.request, 
                                                    widget, 
                                                    widget.field, 
                                                    widget.form, 
                                                    self.context), 
                                                   IErrorViewSnippet)
            view.update()
            widget.error = view
            return view

        data, errors = super(LoadFromSimilarForm,self).extractData()
        isbn = self.getISBN(data)
        print "- isbn: ", isbn
        if isbn:
            isbnWidget = self.widgets.get('load_isbn',None)
            valid = is_valid_isbn(isbn)
            if not valid:
                # validity error
                print "isbn is not valid"
                errors += (getErrorView(isbnWidget, Invalid(u'Chyba v ISBN')),)
                pass
            else:
                try:
                    appearedAtAleph = getISBNCount(isbn, base='nkc')
                    print "- appeared at aleph: ", appearedAtAleph
                    if not appearedAtAleph:
                        print "isbn does not appeared in Aleph"
                        errors += (getErrorView(isbnWidget, 
                                                Invalid(u'ISBN v Alephu neexistuje. Použijte jiné.')),)
                except:
                    print "some exception with edeposit.amqp.aleph.aleph.getISBNCount"
                    pass
            pass
        return (data,errors)


    @button.buttonAndHandler(u"Předvyplnit formulář", name='load')
    def handleLoad(self, action):
        print "LoadFromSimilarForm - handleLoad"
        data, errors = self.extractData()
        if errors:
            return

        isbn = self.getISBN(data)
        records = loadFromAlephByISBN(isbn)
        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)

        if session.get('load_isbn',"some isbn") != isbn:
            session.set('load_isbn',isbn)
            session.set('aleph_records',records)
            self.updateWidgets()
            return

        if not session.get('aleph_records',[]):
            session.set('aleph_records',records)
            self.updateWidgets()
            return

        def hasProperNumberFactory(docNumber):
            def predicate(record):
                return record.docNumber == docNumber
            return predicate
            
        proper_records = filter(hasProperNumberFactory(data['proper_sysnumber']), records)
        proper_record = proper_records and proper_records[0]
        session.set('proper_record',proper_record)
        session.set('aleph_records',[])

        url = os.path.join(self.context.absolute_url(),"aleph-record-loaded")
        #url = os.path.join(self.context.absolute_url(),"add-at-once")
        self.response.redirect(url)
        pass
    pass

LoadFromSimilarView = wrap_form(LoadFromSimilarForm)

class LoadFromSimilarSubView(FormWrapper):
     """ Form view which renders z3c.forms embedded in a portlet.
     Subclass FormWrapper so that we can use custom frame template. """
     index = ViewPageTemplateFile("formwrapper.pt")

class AlephRecordLoaded(BrowserView):
    pass

class IChooseAlephRecord(form.Schema):
    load_isbn = schema.ASCIILine(
        title = u'ISBN v dotazu',
        description = u'Podle tohoto ISBN se načítají údaje',
        required = False,
        readonly = False,
    )
    proper_sysnumber = schema.Choice (
        title = u'Správný záznam',
        source = records_to_choose_from
    )

@form.default_value(field=IChooseAlephRecord['load_isbn'])
def isbnFromSession(data):
    sdm = data.context.session_data_manager
    session = sdm.getSessionData(create=True)
    load_isbn = session.get('load_isbn',"")
    return load_isbn


class SubmitAlephRecordForm(form.SchemaForm):
    grok.context(IePublicationFolder)
    grok.name('submit-aleph-record')
    grok.require('edeposit.AddEPublication')

    schema = IChooseAlephRecord
    ignoreContext = True
    prefix = "submit-aleph-record."

    @button.buttonAndHandler(u"Načíst", name='submit')
    def handleSubmit(self, action):
        data, errors = super(SubmitAlephRecordForm,self).extractData()
        if errors:
            return

        sdm = self.context.session_data_manager
        session = sdm.getSessionData(create=True)
        isbnAtSession = session.get('load_isbn')

        def hasProperNumberFactory(docNumber):
            def predicate(record):
                return record.docNumber == docNumber
            return predicate
            
        proper_records = filter(hasProperNumberFactory(data['proper_sysnumber']), 
                                session.get('aleph_records',[]))
        proper_record = proper_records and proper_records[0]
        if proper_record:
            session.set('proper_record',proper_record)
            url = os.path.join(self.context.absolute_url(),"aleph-record-loaded")
            print "redirect to: ", url
            self.response.redirect(url)
        pass

SubmitAlephRecordView = wrap_form(SubmitAlephRecordForm)
