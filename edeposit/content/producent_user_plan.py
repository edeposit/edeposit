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

from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from plone.dexterity.utils import createContentInContainer

from z3c.relationfield.schema import RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder

from edeposit.content import MessageFactory as _

@grok.provider(IContextSourceBinder)
def availableEditors(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.user.producentuser",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)


# Interface class; used to define content-type schema.

class IProducentUserPlan(form.Schema, IImageScaleTraversable):
    """
    E-Deposit: Producent User Plan
    """
    user = RelationChoice( title=u"Zodpovědný pracovník",
                           required = True,
                           source = availableEditors)


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ProducentUserPlan(Item):
    grok.implements(IProducentUserPlan)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# producent_user_plan_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IProducentUserPlan)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
