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

class IAlephRecord(form.Schema, IImageScaleTraversable):
    """
    E-Deposit Aleph Record
    """
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = True,
    )

    def getNazev(self):
        return self.title

    nazev = schema.TextLine (
        title = u"Název",
        required = False,
    )

    podnazev = schema.TextLine (
        title = u"Podnázev",
        required = False,
    )

    cast = schema.TextLine (
        title = u"Část, díl",
        required = False,
    )

    nazev_casti = schema.TextLine (
        title = u"Název části, dílu",
        required = False,
        )

    rok_vydani = schema.ASCIILine (
        title = u"Rok vydání",
        required = True,
    )

    aleph_sys_number = schema.ASCIILine (
        title = _(u'Aleph SysNumber'),
        description = _(u'Internal SysNumber that Aleph refers to metadata of this ePublication'),
        required = True,
    )
    
    aleph_library = schema.ASCIILine (
        title = _(u'Aleph Library'),
        description = _(u'Library that Aleph refers to metadata of this ePublication'),
        required = True,
    )
    hasAcquisitionFields= schema.Bool (
        title = _(u'has Acquisition Fields'),
        description = _(u'This record has acquisition fields.'),
        required = False,
        default = False,
    )
    hasISBNAgencyFields= schema.Bool (
        title = _(u'has ISBN Agency Fields'),
        description = _(u'This record has ISBN Agency fields'),
        required = False,
        default = False,
    )
    hasDescriptiveCataloguingFields= schema.Bool (
        title = _(u'has Descriptive Cataloguing Fields'),
        description = u"",
        required = False,
        default = False,
    )
    hasDescriptiveCataloguingReviewFields= schema.Bool (
        title = _(u'has Descriptive Cataloguing Review Fields'),
        description = u"",
        required = False,
        default = False,
    )
    hasSubjectCataloguingFields= schema.Bool (
        title = _(u'has Subject Cataloguing Fields'),
        description = u"",
        required = False,
        default = False,
    )
    hasSubjectCataloguingReviewFields= schema.Bool (
        title = _(u'has Subject Cataloguing Review Fields'),
        description = u"",
        required = False,
        default = False,
    )
    isClosed= schema.Bool (
        title = _(u'is closed out by Catalogizators'),
        description = u"",
        required = False,
        default = False,
    )
    summary_record_aleph_sys_number  = schema.ASCIILine (
        title = _(u'Aleph SysNumber of Summary Record'),
        description = _(u'Internal SysNumber of a Summary Aleph Record for this ePublication'),
        required = False,
    )
    summary_record_info = schema.ASCIILine (
        title = _(u'Info about Summary Record'),
        description = _(u'Informations about Summary Aleph Record for this ePublication'),
        required = False,
    )
    internal_url = schema.ASCIILine (
        title = _(u'Internal URL'),
        description = _(u'link to eDeposit'),
        required = False,
    )
    xml = NamedBlobFile (
        title=_(u"XML file with MARC21"),
        required = False,
    )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class AlephRecord(Item):
    grok.implements(IAlephRecord)
    
    def findAndLoadChanges(self, data):
        def isChanged(attr):
            return getattr(self,attr,None) != data.get(attr,None)

        changedAttrs = filter(isChanged, data.keys())
        print "changedAttrs", changedAttrs
        for attr in changedAttrs:
            setattr(self, attr, data.get(attr,None) )
        return changedAttrs

# View class
# The view will automatically use a similarly named template in
# aleph_record_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IAlephRecord)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
