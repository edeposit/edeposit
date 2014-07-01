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


from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IBook(form.Schema, IImageScaleTraversable):
    """
    E-Deposit - Book
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
        description = _(u'Fill in a coedition of a book'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    published_at_order = schema.ASCIILine(
        title = _(u'Published at order'),
        description = _(u'Fill in an order a book was published at.'),
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
                  label=_('Technical'),
                  fields = [ 'person_who_processed_this',
                             'aleph_doc_number',
                             ]
                  )
    person_who_processed_this = schema.ASCIILine(
        title = _(u'Person who processed this.'),
        description = _(u'Fill in a name of a person who processed this book.'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    aleph_doc_number = schema.ASCIILine(
        title = _(u'Aleph DocNumber'),
        description = _(u'Internal DocNumber that Aleph refers to metadata of this book'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )

    generated_isbn = schema.Bool(
        title = _(u'Generate ISBN'),
        description = _(u'Whether ISBN agency should generate ISBN number.'),
        required = False,
        readonly = False,
        default = False,
        missing_value = False,
        )

    form.fieldset('riv',
                  label=_(u'RIV'),
                  fields = ['category_for_riv',
                            ])

    category_for_riv = schema.ASCIILine(
        title = _(u'RIV category'),
        description = _(u'Category of a Book for RIV'),
        required = False,
        readonly = False,
        default = None,
        missing_value = None,
        )
    
    


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Book(Container):
    grok.implements(IBook)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# book_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IBook)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
