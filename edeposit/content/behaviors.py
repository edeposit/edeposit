# -*- coding: utf-8 -*-
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import implementer, alsoProvides
from zope.component import adapter
from zope import schema
from edeposit.content.originalfile import IOriginalFile
from plone import api
from edeposit.content import MessageFactory as _
from z3c.form.interfaces import IDisplayForm
import magic
import plone.directives

class IFormat(model.Schema):
    """Add format to content
    """
    format = schema.ASCIILine (
        title=_(u"Format of a file."),
        readonly = True,
        required = False,
    )

    form.order_after(format='file')

    form.no_omit(IDisplayForm,'format')

@implementer(IFormat)
@adapter(IOriginalFile)
class Format(object):
    """Store format in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """

    def __init__(self, context):
        self.context = context

    @property
    def format(self):
        if self.context.file:
            fileFormat = magic.from_buffer(self.context.file.data)
            print "identified: %s for file: %s" % (fileFormat, str(self.context))
            txt = fileFormat.lower()
            shortFormat = (('mobipocket' in txt) and 'Mobi') or \
                          (('epub' in txt) and 'EPub') or \
                          (('pdf' in txt) and 'PDF') or fileFormat
            
            print "format format is: ", shortFormat
            return shortFormat

        return 'text/html'

alsoProvides(IFormat, IFormFieldProvider)

class ICalibreFormat(model.Schema):
    """Add format to content
    """
    format = schema.ASCIILine (
        title=_(u"Format of a file."),
        readonly = True,
        required = False,
    )

from zope.interface import implements
from zope.component import adapts

class CalibreFormat(object):
    implements(ICalibreFormat)
    adapts(IOriginalFile)

    def __init__(self, context):
        self.context = context

    @property
    def format(self):
        format = IFormat(self.context).format
        return format.lower()


class IChangesInformating(model.Schema):
    """ Behavior interface to help to inform producents about changes that appeared.
    """

    plone.directives.form.fieldset('technical', label=u"Technické údaje",
                                   fields=['lastChangesInformationSent', 'informProducentAboutChanges'])
    
    informProducentAboutChanges = schema.Bool (
        title=u"Informovat producenta o změnách v záznamech",
        default=False,
        required=False,
    )
    lastChangesInformationSent = schema.Datetime (
        title = u"Cas posledního odeslání upozornění",
        required = False,
    )

alsoProvides(IChangesInformating, IFormFieldProvider)
