# -*- coding: utf-8 -*-
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
from z3c.relationfield.schema import RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder

from edeposit.content.aleph_record import IAlephRecord
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary


def urlCodeIsValid(value):
    return True

@grok.provider(IContextSourceBinder)
def availableAlephRecords(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.alephrecord",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

class IOriginalFile(form.Schema, IImageScaleTraversable):
    """
    E-Deposit Original File
    """

    url = schema.ASCIILine(
        title=_("URL"),
        constraint=urlCodeIsValid,
        required = False,
        )

    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = False,
        )

    form.primary('file')
    file = NamedBlobFile(
        title=_(u"Original File of an ePublication"),
        required = False,
        )
    
    format = schema.Choice(
        title=_(u"Format of a file."),
        vocabulary="edeposit.content.fileTypes",
        required = False,
    )

    generated_isbn = schema.Bool(
        title = _(u'Generate ISBN'),
        description = _(u'Whether ISBN agency should generate ISBN number.'),
        required = False,
        default = False,
        missing_value = False,
    )

    related_aleph_record = RelationChoice( title=u"Odpovídající záznam v Alephu",
                                           required = False,
                                           source = availableAlephRecords)
                                           
    

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
