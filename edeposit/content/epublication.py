# -*- coding: utf-8 -*-
from five import grok
import zope
from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.lifecycleevent import modified

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder, UUIDSourceBinder
from plone.formwidget.autocomplete import AutocompleteFieldWidget, AutocompleteMultiFieldWidget
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet

from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds

from edeposit.content.library import ILibrary
from edeposit.content import MessageFactory as _

from .author import IAuthor
from .originalfile import IOriginalFile

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

import z3c.form.browser.radio

import edeposit.amqp.aleph
# Interface class; used to define content-type schema.

class IePublication(form.Schema, IImageScaleTraversable):
    """
    E-Deposit ePublication
    """

    # nazev = schema.TextLine (
    #     title = u"Název",
    #     required = True,
    # )

    def getNazev(self):
        return self.title

    podnazev = schema.TextLine (
        title = u"Podnázev",
        required = False,
    )

    cast = schema.TextLine (
        title = u"Část (svazek,díl)",
        required = False,
    )
    
    nazev_casti = schema.TextLine (
        title = u"Název části, dílu",
        required = False,
        )

    isbn_souboru_publikaci = schema.ASCIILine (
        title = u"ISBN souboru publikací",
        description = u"pro vícesvazkové publikace, ISBN celého souboru publikací.",
        required = False,
    )

    poradi_vydani = schema.TextLine(
        title = u'Pořadí vydání',
        required = True,
    )

    misto_vydani = schema.TextLine(
        title = u'Místo vydání',
        required = True,
    )

    rok_vydani = schema.Int (
        title = u"Rok vydání",
        required = True,
    )

    nakladatel_vydavatel = schema.TextLine (
        title = u"Nakladatel/vydavatel",
        required = True,
        )
    
    vydano_v_koedici_s = schema.TextLine(
        title = u'Vydáno v koedici s',
        required = False,
        )

    cena = schema.Decimal (
        title = u'Cena v Kč',
        required = False,
    )

    form.fieldset('riv',
                  label=_(u'RIV'),
                  fields = [
                      'offer_to_riv',
                      'category_for_riv',
                  ])
    offer_to_riv = schema.Bool(
        title = u'Zpřístupnit pro RIV',
        required = False,
        default = False,
        missing_value = False,
        )

    category_for_riv = schema.Choice (
        title = u"Kategorie pro RIV",
        description = u"Vyberte ze seznamu kategorií pro RIV.",
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        vocabulary="edeposit.content.categoriesForRIV",
    )

    form.fieldset('accessing',
                  label=u'Zpřístupnění',
                  fields = ['is_public',
                            'libraries_accessing',
                            'libraries_that_can_access'
                            ])
    is_public = schema.Bool(
        title = u'ePublikace je veřejná',
        required = False,
        default = False,
        missing_value = False,
        )

    form.widget(libraries_accessing=z3c.form.browser.radio.RadioFieldWidget)
    libraries_accessing = schema.Choice (
        title = u"Oprávnění knihovnám",
        required = False,
        readonly = False,
        default =  u'Vybrané knihovny mají přístup',
        missing_value =  u'Vybrané knihovny mají přístup',
        values = [u'Žádná knihovna nemá přístup k ePublikaci',
                  u'Všechny knihovny mají přístup k ePublikaci',
                  u'Vybrané knihovny mají přístup'
              ],
    )

    #form.widget(libraries_that_can_access=AutocompleteMultiFieldWidget)    
    libraries_that_can_access = RelationList(
        title = _(u'Libraries that can access this ePublication'),
        #description = _(u'Choose libraries that can show an ePublication at its terminal.'),
        required = False,
        readonly = False,
        default = [],
        value_type = RelationChoice(
            title = _(u'Related libraries'),
            source = ObjPathSourceBinder(object_provides=ILibrary.__identifier__),
            )
        )

    # puvodni_nazev = schema.TextLine (
    #     title = u"Originální název",
    #     description = u"u síťových publikací obsahujících díla přeložená, nebo záznamy převzaté z jinojazyčné pulikace",
    #     required = False,
    # )
    # verze_vydani_pro_preklad = schema.TextLine (
    #     title = u"Verze vydání ze kterého překlad vychází.",
    #     required = False,
    # )

    vazba = schema.TextLine (
        title = u"Vazba",
        required = False,
        default = u"online",
    )
    
    # url = schema.ASCIILine (
    #     title = u"URL",
    #     description = u"Adresa, kde je publikace zpřístupněna veřejnosti",
    #     required = False,
    # )
    
    # datum_pro_copyright = schema.Date (
    #     title = u"Datum pro copyright",
    #     description = u"Datum 1. vydání",
    #     required = False,
    # )

    # form.fieldset('svazek',
    #               label= u'Část, díl',
    #               fields = ['cast','nazev_casti',]
    # )
    
    # form.fieldset('Distribution',
    #               label=u"Distribuce",
    #               fields = [ 'distributor',
    #                          'datum_distribuce',
    #                          'misto_distribuce',
    #                      ]
    #           )
    # distributor = schema.TextLine (
    #     title = u"Distributor",
    #     required = False,
    # )

    # datum_distribuce = schema.Date (
    #     title = u"Datum distribuce",
    #     required = False,
    #     )
    
    # misto_distribuce = schema.TextLine(
    #     title = u'Místo distribuce',
    #     required = False,
    #     )

    # form.fieldset('technical',
    #               label=_('Technical'),
    #               fields = [ 'zpracovatel_zaznamu',
    #                          'aleph_doc_number',
    #                          ]
    #               )

    # zpracovatel_zaznamu = schema.TextLine(
    #     title = u'Zpracovatel záznamu',
    #     required = True,
    # )

# @form.default_value(field=IePublication['zpracovatel_zaznamu'])
# def zpracovatelDefaultValue(data):
#     member = api.user.get_current()
#     return member.fullname or member.id


@form.default_value(field=IePublication['nakladatel_vydavatel'])
def nakladatelDefaultValue(data):
    producent = data.context.aq_parent
    return producent.title or producent.id
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ePublication(Container):
    grok.implements(IePublication)

    # Add your class methods and properties here
    def updateOrAddAlephRecord(self, dataForFactory):
        wft = api.portal.get_tool('portal_workflow')
        isbn = dataForFactory['isbn']
        sysNumber = dataForFactory['aleph_sys_number']
        originalFiles = self.listFolderContents(contentFilter={"portal_type" : "edeposit.content.originalfile"})

        # najit original-file pro odpovidajici zaznamy
        originalFilesWithGivenISBN = [ of for of in originalFiles if of.isbn == isbn ]
        if not originalFilesWithGivenISBN:
            wft.doActionFor(self,'notifySystemAction', 
                            comment="No original file found for aleph record with isbn: %s, docNumber: %s" % (isbn, str(sysNumber)))
        else:
            for of in originalFilesWithGivenISBN:
                of.updateOrAddAlephRecord(dataForFactory)
            pass
            modified(self)
            wft.doActionFor(self, 'alephRecordLoaded', 
                            comment = "Got an Aleph record with isbn: %s, docNumber: %s" % (isbn, str(sysNumber)))
                
        pass

    def allOriginalFilesHaveRelatedAlephRecord(self):
        originalFiles = self.listFolderContents(contentFilter={"portal_type" : "edeposit.content.originalfile"})
        ofWithoutRelatedAlephRecord = filter(lambda of: not of.related_aleph_record, originalFiles)
        return originalFiles and not ofWithoutRelatedAlephRecord

class IAuthors(model.Schema):
    form.fieldset('authors',
                  label=u'Autoři',
                  fields = [
                      'authors',
                  ])
    authors = zope.schema.List(
        title = u"Autoři",
        required = False,
        value_type = zope.schema.Object( title=u"Autoři", schema=IAuthor ),
        unique = False,
        min_length = 3
    )

class IOriginalFiles(model.Schema):
    originalFiles = zope.schema.List(
        title = u"Soubory s originálem",
        required = False,
        value_type = zope.schema.Object( title=u"Soubory s originálem", schema=IOriginalFile ),
        unique = False,
        min_length = 1
    )

from originalfile import OriginalFile
from epublicationfolder import IePublicationFolder

class EPublicationAddForm(DefaultAddForm):
    label = u"Ohlášení ePublikace"
    # description = _(u"Please fill informations about user and producent.")
    default_fieldset_label = u"ePublikace"
    portal_type="edeposit.content.epublication"
    grok.context(IePublicationFolder)
    enable_form_tabbing = False
    autoGroups = False

    @property
    def additionalSchemata(self):
        schemata = [IOriginalFile,] + \
                   [s for s in getAdditionalSchemata(portal_type=self.portal_type)] + \
                   [IAuthors, ]
        return schemata

    def update(self):
        super(DefaultAddForm,self).update()
        self.widgets['IBasic.title'].label=u"Název ePublikace"
        
    def extractData(self):
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

        data, errors = super(EPublicationAddForm,self).extractData()
        isbn = data.get('IOriginalFile.isbn',None)
        if isbn:
            isbnWidget = self.widgets.get('IOriginalFile.isbn',None)
            valid = edeposit.amqp.aleph.isbn.is_valid_isbn(isbn)
            if not valid:
                # validity error
                print "isbn is not valid"
                errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'Chyba v ISBN')),)
                pass
            else:
                try:
                    appearedAtAleph = edeposit.amqp.aleph.aleph.getISBNCount(isbn)
                    if appearedAtAleph:
                        print "isbn already appeared in Aleph"
                        # duplicity error
                        errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'ISBN je již použito. Použijte jiné, nebo nahlašte opravu.')),)
                except:
                    print "some exception with edeposit.amqp.aleph.aleph.getISBNCount"
                    pass
            pass
        return (data,errors)

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Add New Item operation cancelled"), "info")
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))

    @button.buttonAndHandler(u"Ohlásit", name='save')
    def handleAdd(self, action):
        print "handle add"
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        if (not data['IOriginalFile.isbn'] and not data['IOriginalFile.generated_isbn']) or \
           (data['IOriginalFile.isbn'] and data['IOriginalFileí.geerat,d_isbn']):
            raise ActionExecutionError(Invalid(u"Zadejte prosím ISBN, nebo vyberte \"Přidělit ISBN agenturou\"."))

        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object and not
            # other submitting
            self._finishedAdd = getattr(self,'submitAgain',False) == False
            IStatusMessage(self.request).addStatusMessage(_(u"Item created"), "info")
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(self.new_object, 'submitDeclaration', comment='handled automatically')

    # @button.buttonAndHandler(u'Ohlásit a další', name='submitAgain')
    # def handleSubmitAgain(self, action):
    #     return self.handleAdd(action)

    def add(self,object):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        new_object = addContentToContainer(container, object)
        self.new_object = new_object
        if fti.immediate_view:
            self.immediate_view = "%s/%s/%s" % (container.absolute_url(), new_object.id, fti.immediate_view,)
        else:
            self.immediate_view = "%s/%s" % (container.absolute_url(), new_object.id)

        for author in filter(lambda author: author.fullname, self.authors):
            author.title = author.fullname
            addContentToContainer(new_object, author, True)
            
        if self.originalFile:
            value = self.originalFile
            newOriginalFile = createContentInContainer(new_object,'edeposit.content.originalfile',**value)
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(newOriginalFile, 
                            (newOriginalFile.isbn and 'submitDeclarationToISBNValidation')
                            or (newOriginalFile.file and 'submitDeclarationToAntivirus')
                            or 'submitDeclarationToISBNGenerating',
                            comment='handled automatically')

    def create(self, data):
        def getAndRemoveKey(data, key, defaultValue):
            if key in data:
                value = data[key]
                del data[key]
                return value
            else:
                return defaultValue
                
        self.authors = getAndRemoveKey(data,'IAuthors.authors',[]) or []
        self.originalFile = dict(map(lambda key: (key, getAndRemoveKey(data,'IOriginalFile.' + key,None)),
                                     IOriginalFile.names()))
        self.submittedData = data
        self.submitAgain = self.request.get('REPEAT','N') == 'Y'
        created = DefaultAddForm.create(self,data)
        return created

class EPublicationAddView(DefaultAddView):
    form = EPublicationAddForm
    pass

class AuthorFactory(object):
    adapts(Interface, Interface, Interface, Interface)
    zope.interface.implements(IObjectFactory)
    
    def __init__(self, context, request, form, widget):
        self.context = context
        self.request = request
        self.form = form
        self.widget = widget

    def __call__(self, value):
        created=createContent('edeposit.content.author',**value)
        return created

class OriginalFileFactory(object):
    adapts(Interface, Interface, Interface, Interface)
    zope.interface.implements(IObjectFactory)
    
    def __init__(self, context, request, form, widget):
        self.context = context
        self.request = request
        self.form = form
        self.widget = widget


    def __call__(self, value):
        created=createContent('edeposit.content.originalfile',**value)
        created.portal_quickinstaller = api.portal.get_tool('portal_quickinstaller')
        created.portal_url = api.portal.get_tool('portal_url')
        return created


# View class
# The view will automatically use a similarly named template in
# epublication_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

@grok.provider(IContextSourceBinder)
def availableLibraries(context):
    path = '/libraries' #.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.library",),
              "path": {'query' :path } 
             }
    libraries = api.portal.get_tool('portal_catalog')(portal_type='edeposit.content.library')
    def getTerm(library):
        title = library.Title.encode('utf-8')
        return SimpleVocabulary.createTerm(library.id, library.id, title)

    #return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)
    return SimpleVocabulary(map(getTerm, libraries))

class IAddAtOnceForm(form.Schema):
    nazev = schema.TextLine (
        title = u"Název ePublikace",
        required = True,
        )

    podnazev = schema.TextLine (
        title = u"Podnázev",
        required = False,
        )

    cast = schema.TextLine (
        title = u"Část (svazek,díl)",
        required = False,
    )
    
    nazev_casti = schema.TextLine (
        title = u"Název části, dílu",
        required = False,
        )
    
    isbn = schema.ASCIILine(
        title=u"ISBN (pokud je)",
        required = False,
        )

    isbn_souboru_publikaci = schema.ASCIILine (
        title = u"ISBN souboru (pro vícesvazkové dokumenty)",
        required = False,
    )
    
    generated_isbn = schema.Bool(
        title = u'Přidělit agenturou ISBN',
        required = False,
        default = False,
        missing_value = False,
        )

    author1 = schema.TextLine(
        title=u"Autor (příjmení, křestní jméno)",
        required = False,
        )
    
    author2 = schema.TextLine(
        title=u"Autor 2",
        required = False,
        )
    
    author3 = schema.TextLine(
        title=u"Autor 3",
        required = False,
        )

    poradi_vydani = schema.TextLine(
        title = u'Pořadí vydání, verze',
        required = True,
    )

    misto_vydani = schema.TextLine(
        title = u'Místo vydání',
        required = True,
    )

    rok_vydani = schema.Int (
        title = u"Rok vydání",
        required = True,
    )

    form.mode(nakladatel_vydavatel='display')
    nakladatel_vydavatel = schema.TextLine (
        title = u"Nakladatel",
        required = True,
        )
    
    vydano_v_koedici_s = schema.TextLine(
        title = u'Vydáno v koedici s',
        required = False,
        )

    cena = schema.Decimal (
        title = u'Cena v Kč',
        required = False,
    )

    # form.fieldset('riv',
    #               label=_(u'RIV'),
    #               fields = [
    #                   'offer_to_riv',
    #                   'category_for_riv',
    #               ])
    offer_to_riv = schema.Bool(
        title = u'Zpřístupnit pro RIV',
        required = False,
        default = False,
        missing_value = False,
        )

    category_for_riv = schema.Choice (
        title = u"Kategorie pro RIV",
        description = u"Vyberte ze seznamu kategorií pro RIV.",
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        vocabulary="edeposit.content.categoriesForRIV",
    )

    # form.fieldset('accessing',
    #               label=u'Zpřístupnění',
    #               fields = ['is_public',
    #                         'libraries_accessing',
    #                         'libraries_that_can_access'
    #                         ])
    is_public = schema.Bool(
        title = u'ePublikace je veřejná',
        required = False,
        default = False,
        missing_value = False,
        )

    form.widget(libraries_accessing=z3c.form.browser.radio.RadioFieldWidget)
    libraries_accessing = schema.Choice (
        title = u"Oprávnění knihovnám",
        required = False,
        readonly = False,
        default =  u'Vybrané knihovny mají přístup',
        missing_value =  u'Vybrané knihovny mají přístup',
        values = [u'Žádná knihovna nemá přístup k ePublikaci',
                  u'Všechny knihovny mají přístup k ePublikaci',
                  u'Vybrané knihovny mají přístup'
              ],
    )

    libraries_that_can_access = schema.Set(
        title = u"Knihovny s přístupem k ePublikaci", #(u'Libraries that can access this ePublication'),
        required = False,
        readonly = False,
        value_type = schema.Choice(source=availableLibraries)
        )
    
    # #form.widget(libraries_that_can_access=AutocompleteMultiFieldWidget)    
    # libraries_that_can_access = RelationList(
    #     title = _(u'Libraries that can access this ePublication'),
    #     required = False,
    #     readonly = False,
    #     default = [],
    #     value_type = RelationChoice(
    #         title = _(u'Related libraries'),
    #         source = availableLibraries,
    #         )
    #     )

    zpracovatel_zaznamu = schema.TextLine(
        title = u'Zpracovatel záznamu',
        required = True,
    )

    url = schema.ASCIILine (
        title = u"URL (pokud je ke stažení z internetu)",
        required = False,
    )

    file = NamedBlobFile(
        title=u"Připojit soubor s ePublikací",
        required = False,
        )
    
    format = schema.Choice(
        title=_(u"Format of a file."),
        vocabulary="edeposit.content.fileTypes",
        required = False,
        )

    poznamka = schema.Text(
        title = u"Poznámka",
        required = False,
        )

    form.mode(epublication_uid='hidden')
    epublication_uid = schema.ASCIILine(
        required = False,
        )
    

@form.default_value(field=IAddAtOnceForm['zpracovatel_zaznamu'])
def zpracovatelDefaultValue(data):
    member = api.user.get_current()
    return member.fullname or member.id


@form.default_value(field=IAddAtOnceForm['nakladatel_vydavatel'])
def nakladatelDefaultValue(data):
    producent = data.context.aq_parent
    return producent.title or producent.id

class AddAtOnceForm(form.SchemaForm):
    grok.name('add-at-once')
    grok.require('edeposit.AddEPublication')
    grok.context(IePublicationFolder)
    schema = IAddAtOnceForm
    ignoreContext = True
    label = u"Ohlásit ePublikaci"
    enable_form_tabbing = False
    autoGroups = False

    def extractData(self):
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

        data, errors = super(AddAtOnceForm,self).extractData()
        isbn = data.get('isbn',None)
        if isbn:
            isbnWidget = self.widgets.get('isbn',None)
            valid = edeposit.amqp.aleph.isbn.is_valid_isbn(isbn)
            if not valid:
                # validity error
                print "isbn is not valid"
                errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'Chyba v ISBN')),)
                pass
            else:
                try:
                    appearedAtAleph = edeposit.amqp.aleph.aleph.getISBNCount(isbn)
                    if appearedAtAleph:
                        print "isbn already appeared in Aleph"
                        # duplicity error
                        errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'ISBN je již použito. Použijte jiné, nebo nahlašte opravu.')),)
                except:
                    print "some exception with edeposit.amqp.aleph.aleph.getISBNCount"
                    pass
            pass
        return (data,errors)

    def checkISBN(self, data):
        if (not data['isbn'] and not data['generated_isbn']) or \
           (data['isbn'] and data['generated_isbn']):
            raise ActionExecutionError(Invalid(u"Buď zadejte ISBN, nebo vyberte \"Přiřadit ISBN agenturou\""))
        
    def createContentFromData(self, interface, portal_type, data, additionalData = {}, exceptKeys = []):
        theSameKeys = frozenset(interface.names()).intersection(data.keys()) - frozenset(exceptKeys)
        dataFromTheSameKeys = [(key,data[key]) for key in theSameKeys]
        dataForFactory = dict(dataFromTheSameKeys + additionalData.items())
        return createContent(portal_type, **dataForFactory)

    def addOriginalFile(self, newEPublication, data):
        originalFileTitle = "%s (%s)" % (data['nazev'], data['file'] and data['file'].filename or "")
        newOriginalFile = addContentToContainer( newEPublication,
                                                 self.createContentFromData(IOriginalFile, 'edeposit.content.originalfile', data,
                                                                            dict(title=originalFileTitle,
                                                                                 allow_discussion = True,
                                                                                 ),
                                                                            )
                                                 )
        comment = data.get('poznamka',"")
        if comment:
            commentObj = createObject('plone.Comment')
            commentObj.text = comment
            commentObj.user_notification = False

            member = api.user.get_current()
            commentObj.author_username = member.getUserName()
            commentObj.author_name = member.getProperty('fullname') or member.getUserName()
            
            conversation=IConversation(newOriginalFile)
            conversation.addComment(commentObj)

        wft = api.portal.get_tool('portal_workflow')
        wft.doActionFor( newOriginalFile, 
                         (newOriginalFile.isbn and 'submitDeclarationToISBNValidation')
                         or (newOriginalFile.file and 'submitDeclarationToAntivirus')
                         or 'submitDeclarationToISBNGenerating',
                         comment='handled automatically')
        return newOriginalFile

    def addEPublication(self, data):
        container = aq_inner(self.context)        
        newEPublication = addContentToContainer( container,
                                                 self.createContentFromData(IePublication, 'edeposit.content.epublication', data, 
                                                                            dict(vazba='online',title=data['nazev']), 
                                                                            ['libraries_that_can_access',])
                                                 )
        return newEPublication

    @button.buttonAndHandler(u"Odeslat", name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.checkISBN(data)

        newEPublication = data.get('epublication_uid') and api.content.get(UID=data['epublication_uid']) \
            or self.addEPublication(data)

        newOriginalFile = self.addOriginalFile(newEPublication, data)

        if not data.get('epublication_uid'):
            authors = [data[key] for key in ['author1','author2','author3'] if data[key]]
            for author in authors:
                createContentInContainer(newEPublication, 'edeposit.content.author', fullname=author, title=author)

        messages = IStatusMessage(self.request)
        messages.addStatusMessage(u"ePublikace byla ohlášena.", type="info")

        fti = getUtility(IDexterityFTI, name=newOriginalFile.portal_type)
        #returnURL = "/".join([container.absolute_url(), newEPublication.id, newOriginalFile.id, fti.immediate_view])
        self.request.response.redirect(newOriginalFile.absolute_url())

    @button.buttonAndHandler(u"Odeslat a ohlásit ještě jednou s jiným ISBN", name='save-and-next')
    def handleAddAndNext(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.checkISBN(data)

        newEPublication = data.get('epublication_uid') and api.content.get(UID=data['epublication_uid']) \
            or self.addEPublication(data)

        self.widgets['epublication_uid'].value=newEPublication.UID()

        newOriginalFile = self.addOriginalFile(newEPublication, data)
        if not data.get('epublication_uid'):
            authors = [data[key] for key in ['author1','author2','author3'] if data[key]]
            for author in authors:
                createContentInContainer(newEPublication, 'edeposit.content.author', fullname=author, title=author)

        # # set mode display all fields for epublication and authors
        # readOnlyFields = list(frozenset(data.keys()).intersection(frozenset(IePublication.names()))) + \
        #     ['author%d' % (num,) for num in (1,2,3)] + ['nazev',]

        # for fieldName in readOnlyFields:
        #     widget = self.widgets.get(fieldName)
        #     if widget:
        #         widget.mode = 'display'
        #     pass

        # vycistime policka pro originalfile
        self.widgets['isbn'].value = ""

        messages = IStatusMessage(self.request)
        messages.addStatusMessage(u"ePublikace byla ohlášena.", type="info")
        pass
