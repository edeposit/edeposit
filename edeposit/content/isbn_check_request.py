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

class IISBNCheckRequest(form.Schema, IImageScaleTraversable):
    """
    Count ISBN occurrences in Aleph
    """
    isbn = schema.TextLine (
        title = u"ISBN ke zjistění duplicity",
        required = True,
        )

    sent = schema.Datetime(
        title = u'Čas odeslání požadavku',
        required = False,
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ISBNCheckRequest(Item):
    grok.implements(IISBNCheckRequest)

    # Add your class methods and properties here
    pass

