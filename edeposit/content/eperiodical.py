from five import grok

from z3c.form import group, field
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

from edeposit.content.library import ILibrary

from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IePeriodical(form.Schema, IImageScaleTraversable):
    """
    E-Deposit - ePeriodical
    """
    subtitle = schema.ASCIILine (
        title = _(u"Subtitle"),
        required = False,
        )

    edition = schema.ASCIILine (
        title = _(u"Edition"),
        required = False,
        )

    form.fieldset('Publishing',
                  label=_(u"Publishing"),
                  fields = [ 'publisher',
                             'published_with_coedition',
                             'published_at_order',
                             'place_of_publishing',
                             ]
                  )
    place_of_publishing = schema.ASCIILine (
        title = _(u"Place of Publishing"),
        required = False,
        )

    publisher = schema.ASCIILine (
        title = _(u"Publisher"),
        required = False,
        )

    published_with_coedition = schema.ASCIILine(
        title = _(u'Published with Coedition'),
        description = _(u'Fill in a coedition of an ePublication'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    published_at_order = schema.ASCIILine(
        title = _(u'Published at order'),
        description = _(u'Fill in an order an ePublication was published at.'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )
    

    form.fieldset('volume',
                  label=_(u'Volume'),
                  fields = ['volume','volume_title','volume_number']
                  )
    volume = schema.ASCIILine (
        title = _(u"Volume"), # svazek
        required = False,
        )
    
    volume_title = schema.ASCIILine (
        title = _(u"Volume Title"),
        required = False,
        )
    
    volume_number = schema.ASCIILine (
        title = _(u"Volume Number"),
        required = False,
        )

    form.fieldset('technical',
                  label=_('Technical'),
                  fields = [ 'person_who_processed_this',
                             'aleph_doc_number',
                             ]
                  )
    person_who_processed_this = schema.ASCIILine(
        title = _(u'Person who processed this.'),
        description = _(u'Fill in a name of a person who processed this ePeriodical.'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    aleph_doc_number = schema.ASCIILine(
        title = _(u'Aleph DocNumber'),
        description = _(u'Internal DocNumber that Aleph refers to metadata of this ePeriodical'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    form.fieldset('accessing',
                  label=_(u'Accessing'),
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

    form.fieldset('riv',
                  label=_(u'RIV'),
                  fields = ['category_for_riv',
                            ])

    category_for_riv = schema.ASCIILine(
        title = _(u'RIV category'),
        description = _(u'Category of an ePublication for RIV'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ePeriodical(Container):
    grok.implements(IePeriodical)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# eperiodical_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IePeriodical)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
