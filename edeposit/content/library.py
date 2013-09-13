from five import grok
from plone.supermodel import model
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

def urlCodeIsValid(value):
    return True

# Interface class; used to define content-type schema.

class ILibrary(form.Schema, IImageScaleTraversable):
    """
    Informations about library
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/library.xml to define the content type.

    model.fieldset('url',
                   label=_(u"URLs"),
                   fields=['url','url_of_kramerius'])
    url = schema.ASCIILine(
        title=_("URL"),
        description=_(u"URL of a library"),
        constraint=urlCodeIsValid,
        required = False,
        )

    url_of_kramerius = schema.ASCIILine(
        title=_("URL of Kramerius"),
        description=_(u"URL where you can work with Kramerius"),
        constraint=urlCodeIsValid,
        required = False,
        )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class Library(Container):
    grok.implements(ILibrary)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# library_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ILibrary)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
