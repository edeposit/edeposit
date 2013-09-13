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

from edeposit.content.library import ILibrary
from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IePublication(form.Schema, IImageScaleTraversable):
    """
    E-Deposit ePublication
    """

    book_binding = schema.ASCIILine(
        title = _(u"Book Binding"),
        description = _(u"Fill in binding of a book."),
        required = False,
        )
    
    subtitle = schema.ASCIILine (
        title = _(u"Subtitle"),
        required = False,
        )
    form.fieldset('Publishing',
                  label=_(u"Publishing"),
                  fields = [ 'publisher',
                             'date_of_publishing',
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

    date_of_publishing = schema.Date (
        title = _(u"Publishing Date"),
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

    price = schema.Decimal(
        title = _(u"Price"),
        required = False,
        )

    currency = schema.Choice(
        title = _(u'Currency'),
        description = _(u'Fill in currency of a price.'),
        vocabulary='edeposit.content.currencies'
        )

    edition = schema.ASCIILine (
        title = _(u"Edition"),
        required = False,
        )

    edition = schema.ASCIILine (
        title = _(u"Edition"),
        required = False,
        )

    form.fieldset('technical',
                  label=_(''),
                  fields = [ 'person_who_processed_this',
                             'aleph_doc_number',
                             ]
                  )
    person_who_processed_this = schema.ASCIILine(
        title = _(u'Person who processed this.'),
        description = _(u'Fill in a name of a person who processed this ePublication.'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    aleph_doc_number = schema.ASCIILine(
        title = _(u'Aleph DocNumber'),
        description = _(u'Internal DocNumber that Aleph refers to metadata of this ePublication'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    form.fieldset('accessing',
                  label=_(u''),
                  fields = ['libraries_that_can_access_at_library_terminal',
                            'libraries_that_can_access_at_public',
                            ])
    libraries_that_can_access_at_library_terminal = RelationList(
        title = _(u'Libraries that can access at library terminal'),
        description = _(u'Choose libraries that can show an ePublication at its terminal.'),
        required = False,
        readonly = False,
        default = [],
        value_type = RelationChoice(
            title = _(u'Related'),
            source = UUIDSourceBinder(object_provides=ILibrary.__identifier__),
            )
        )
    
    libraries_that_can_access_at_public = RelationList(
        title = _(u'Libraries that can access at public'),
        description = _(u'Choose libraries that can show an ePublication at public.'),
        required = False,
        readonly = False,
        default = [],
        value_type = RelationChoice(
            title = _(u'Related'),
            source = UUIDSourceBinder(object_provides=ILibrary.__identifier__),
            )
        )
                  
# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ePublication(Container):
    grok.implements(IePublication)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# epublication_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IePublication)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
