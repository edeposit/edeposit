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
from z3c.relationfield.schema import RelationChoice, Relation, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder

from edeposit.content.aleph_record import IAlephRecord
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from plone.dexterity.utils import createContentInContainer
from zope.component import queryUtility
from plone import api

from edeposit.content.originalfile import IOriginalFile

@grok.provider(IContextSourceBinder)
def availableDescriptiveCataloguers(context):
    acl_users = getToolByName(context, 'acl_users')
    group = acl_users.getGroupById('Descriptive Cataloguers')
    terms = []

    if group is not None:
        for member_id in group.getMemberIds():
            user = acl_users.getUserById(member_id)
            if user is not None:
                member_name = user.getProperty('fullname') or member_id
                terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

    return SimpleVocabulary(terms)

@grok.provider(IContextSourceBinder)
def availableOriginalFiles(context):
    path = '/'.join(context.getPhysicalPath())
    query = { 
        "portal_type" : "edeposit.content.originalfile",
    }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IDescriptiveCatalogizationWorkPlan(form.Schema):
    """
    E-Deposit: Catalogization Work Plan
    """

    related_catalogizator = schema.Choice( title=u"Pracovník jmenné katalogizace",
                                           required = True,
                                           source = availableDescriptiveCataloguers )
    
    assigned_originalfiles = RelationList(
        title=u"Dokumenty ke zpracování",
        required = False,
        default = [],
        value_type =   RelationChoice( 
            title=u"Originály",
            source = ObjPathSourceBinder(object_provides=IOriginalFile.__identifier__)
        )
    )
    
# @form.default_value(field=ICatalogizationWorkPlan['related_catalogizator'])
# def defaultCatalogizator(data):
#     return "jans"

