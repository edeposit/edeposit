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


class ICalibreFormat(model.Schema):
    """Add format to content
    """
    format = schema.ASCIILine (
        title=_(u"Format of a file."),
        readonly = True,
        required = False,
    )

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
