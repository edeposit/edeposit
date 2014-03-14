# -*- coding: utf-8 -*-
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Item

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable


from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IISBNCountRequest(form.Schema, IImageScaleTraversable):
    """
    Count ISBN occurrences in Aleph
    """
    isbn = schema.TextLine (
        title = u"ISBN ke zjistění duplicity",
        required = True,
        )

    uuid = schema.TextLine (
        title = u"UUID odeslané zprávy",
        required = True,
        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ISBNCountRequest(Item):
    grok.implements(IISBNCountRequest)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# isbn_count_request_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IISBNCountRequest)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
