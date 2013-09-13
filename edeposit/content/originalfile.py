from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.supermodel import model

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from edeposit.content import MessageFactory as _


def urlCodeIsValid(value):
    return True

class IOriginalFile(form.Schema, IImageScaleTraversable):
    """
    E-Deposit Original File
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/originalfile.xml to define the content type.

    url = schema.ASCIILine(
        title=_("URL"),
        description=_(u"URL of a file source."),
        constraint=urlCodeIsValid,
        required = False,
        )
    
    #form.primary('file')
    file = NamedBlobFile(
        title=_(u"Original File of an ePublication"),
        description=_(u"Fill in a file that contains of an epublication"),
        required = True,
        )
    
    format = schema.Choice(
        title=_(u"Format of a file."),
        vocabulary="edeposit.content.fileTypes"
        )

# @form.default_value(field=IOriginalFile['title'])
# def default_title(data):
#     return _(u'original')

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class OriginalFile(Container):
    grok.implements(IOriginalFile)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# originalfile_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IOriginalFile)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
