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

class IAuthor(form.Schema, IImageScaleTraversable):
    """
    Author of ePublication
    """
    form.fieldset('name',
                   label=_(u"Name"),
                   fields=['first_name','last_name'])
    # form.model("models/library.xml")
    first_name = schema.TextLine(
        title=_("First Name"),
        description=_(u"Fill in your first name."),
        required = True,
        )

    last_name = schema.TextLine(
        title=_("Last Name"),
        description=_(u"Fill in your last name."),
        required = True,
        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Author(Container):
    grok.implements(IAuthor)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# author_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IAuthor)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
