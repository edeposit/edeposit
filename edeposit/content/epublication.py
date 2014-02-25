# -*- coding: utf-8 -*-
from five import grok
import zope
from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

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

from edeposit.content.library import ILibrary
from edeposit.content import MessageFactory as _

from .author import IAuthor
from .originalfile import IOriginalFile

from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView
from plone.supermodel import model
from plone.dexterity.utils import getAdditionalSchemata
from Acquisition import aq_inner, aq_base

from zope.component import adapts
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import Invalid, Interface
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory
from plone.dexterity.interfaces import IDexterityFTI
from collections import namedtuple
from plone import api

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

    # vazba = schema.TextLine (
    #     title = u"Vazba",
    #     required = False,
    # )
    
    cena = schema.Decimal (
        title = u'Cena',
        required = False,
    )

    # isbn = schema.ASCIILine (
    #     title = u"ISBN",
    #     description = u"ISNB knižního vydání",
    #     required = False,
    # )

    isbn_souboru_publikaci = schema.ASCIILine (
        title = u"ISBN souboru publikací",
        required = False,
    )

    url = schema.ASCIILine (
        title = u"URL",
        required = False,
    )
    
    datum_pro_copyright = schema.Date (
        title = u"Datum pro copyright",
        required = False,
    )

    form.fieldset('svazek',
                  label= u'Část, díl',
                  fields = ['cast','nazev_casti',]
    )
    cast = schema.TextLine (
        title = u"Část, díl",
        required = False,
    )
    
    nazev_casti = schema.TextLine (
        title = u"Název části, dílu",
        required = False,
        )
    
    form.fieldset('Publishing',
                  label=_(u"Publishing"),
                  fields = [ 'nakladatel_vydavatel',
                             'datum_vydani',
                             'poradi_vydani',
                             'misto_vydani',
                         ]
                  )
    nakladatel_vydavatel = schema.TextLine (
        title = u"Nakladatel/vydavatel",
        required = False,
        )

    datum_vydani = schema.Date (
        title = u"Datum vydání",
        required = False,
        )
    
    poradi_vydani = schema.TextLine(
        title = u'Pořadí vydání',
        required = False,
        )

    misto_vydani = schema.TextLine(
        title = u'Místo vydání',
        required = False,
        )

    form.fieldset('Distribution',
                  label=u"Distribuce",
                  fields = [ 'distributor',
                             'datum_distribuce',
                             'misto_distribuce',
                         ]
              )
    distributor = schema.TextLine (
        title = u"Distributor",
        required = False,
    )

    datum_distribuce = schema.Date (
        title = u"Datum distribuce",
        required = False,
        )
    
    misto_distribuce = schema.TextLine(
        title = u'Místo distribuce',
        required = False,
        )

    form.fieldset('technical',
                  label=_('Technical'),
                  fields = [ 'zpracovatel_zaznamu',
                             'aleph_doc_number',
                             ]
                  )
    zpracovatel_zaznamu = schema.TextLine(
        title = u'Zpracovatel záznamu',
        required = False,
        )

    aleph_doc_number = schema.ASCIILine(
        title = _(u'Aleph DocNumber'),
        description = _(u'Internal DocNumber that Aleph refers to metadata of this ePublication'),
        required = False,
        )

    generated_isbn = schema.Bool(
        title = _(u'Generate ISBN'),
        description = _(u'Whether ISBN agency should generate ISBN number.'),
        required = False,
        default = False,
        missing_value = False,
        )

    form.fieldset('accessing',
                  label=u'Zpřístupnění',
                  fields = ['libraries_that_can_access_at_library_terminal',
                            'libraries_that_can_access_at_public',
                            ])
    #form.widget(libraries_that_can_access_at_library_terminal=AutocompleteMultiFieldWidget)    
    libraries_that_can_access_at_library_terminal = RelationList(
        title = _(u'Libraries that can access at library terminal'),
        description = _(u'Choose libraries that can show an ePublication at its terminal.'),
        required = False,
        readonly = False,
        default = [],
        value_type = RelationChoice(
            title = _(u'Related libraries'),
            source = ObjPathSourceBinder(object_provides=ILibrary.__identifier__),
            )
        )
    #form.widget(libraries_that_can_access_at_public=AutocompleteMultiFieldWidget)    
    libraries_that_can_access_at_public = RelationList(
        title = _(u'Libraries that can access at public'),
        description = _(u'Choose libraries that can show an ePublication at public.'),
        required = False,
        readonly = False,
        default = [],
        value_type = RelationChoice(
            title = _(u'Related libraries at public'),
            source = ObjPathSourceBinder(object_provides=ILibrary.__identifier__),
            )
        )

    # form.fieldset('riv',
    #               label=_(u'RIV'),
    #               fields = [
    #                   'offer_to_riv',
    #                   'category_for_riv',
    #               ])
    offer_to_riv = schema.Bool(
        title = u'Zpřístupnit pro RIV',
        description = u'Chceme aby RIV ePublikaci hodnotil.',
        required = False,
        default = False,
        missing_value = False,
        )

    category_for_riv = schema.Choice (
        title = _(u'RIV category'),
        description = _(u'Category of an ePublication for RIV'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        vocabulary="edeposit.content.categoriesForRIV",
    )
    
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ePublication(Container):
    grok.implements(IePublication)

    # Add your class methods and properties here

class IAuthors(model.Schema):
    authors = zope.schema.List(
        title = u"Autoři",
        required = False,
        value_type = zope.schema.Object( title=u"Autoři", schema=IAuthor ),
        unique = False
    )

class IOriginalFiles(model.Schema):
    originalFiles = zope.schema.List(
        title = u"Soubory s originálem",
        required = False,
        value_type = zope.schema.Object( title=u"Soubory s originálem", schema=IOriginalFile ),
        unique = False
    )

from originalfile import OriginalFile

class EPublicationAddForm(DefaultAddForm):
    # label = _(u"Registration of a producent")
    # description = _(u"Please fill informations about user and producent.")
    default_fieldset_label = u"ePublikace"

    @property
    def additionalSchemata(self):
        schemata = [s for s in getAdditionalSchemata(portal_type=self.portal_type)] + \
                   [IAuthors, IOriginalFiles]
        return schemata

    def update(self):
        DefaultAddForm.update(self)
        self.widgets['IBasic.title'].label=u"Název ePublikace"

    def add(self,object):
        fti = getUtility(IDexterityFTI, name=self.portal_type)
        container = aq_inner(self.context)
        #import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        new_object = addContentToContainer(container, object)
        
        if fti.immediate_view:
            self.immediate_view = "%s/%s/%s" % (container.absolute_url(), new_object.id, fti.immediate_view,)
        else:
            self.immediate_view = "%s/%s" % (container.absolute_url(), new_object.id)

        for author in self.authors:
            author.title = " ".join([author.first_name, author.last_name])
            addContentToContainer(new_object, author, True)
            
        for originalFile in self.originalFiles:
            value = {'file':originalFile.file, 
                     'url': originalFile.url, 
                     'isbn': originalFile.isbn, 
                     'format':originalFile.format}
            createContentInContainer(new_object,'edeposit.content.originalfile',**value)

    def create(self, data):
        def getAndRemoveKey(data, key, defaultValue):
            if key in data:
                value = data[key]
                del data[key]
                return value
            else:
                return defaultValue

        self.authors = getAndRemoveKey(data,'IAuthors.authors',[]) or []
        self.originalFiles = getAndRemoveKey(data,'IOriginalFiles.originalFiles',[]) or []
        created = DefaultAddForm.create(self,data)
        return created

class EPublicationAddView(DefaultAddView):
    form = EPublicationAddForm

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

# class EditAtOnce(grok.View):
#     """ sample view class """
#     grok.context(IePublication)
#     grok.require('zope2.View')
#     grok.name('edit-at-once')
#     # Add view methods here

# class ViewAtOnce(grok.View):
#     """ sample view class """
#     grok.context(IePublication)
#     grok.require('zope2.View')
#     grok.name('view-at-once')
    # Add view methods here
    
    
