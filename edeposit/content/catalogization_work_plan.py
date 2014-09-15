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

def urlCodeIsValid(value):
    return True

@grok.provider(IContextSourceBinder)
def availableCatalogizators(context):
    registry = queryUtility(IRegistry)

    terms = []
    import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

    # for pizza in registry.get('example.dexterityforms.pizzaTypes', ()):
    #     terms.append(SimpleVocabulary.createTerm(pizza, pizza.encode('utf-8'), pizza))

    return SimpleVocabulary(terms)

@grok.provider(IContextSourceBinder)
def availableOriginalFiles(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.originalfile",),
              "path" : {'query': "/producents"}
          }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class ICatalogizationWorkPlan(form.Schema, IImageScaleTraversable):
    """
    E-Deposit: Catalogization Work Plan
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/catalogization_work_plan.xml to define the content type.

    related_catalogizator = RelationChoice( title=u"Pracovník katalogizace",
                                            required = True,
                                            source = availableCatalogizators)

    assigned_originalfiles = RelationList(
        title=u"Dokumenty ke zpracování",
        required = False,
        default = [],
        value_type =   RelationChoice( 
            title=u"Originály",
            source = availableOriginalFiles
        )
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class CatalogizationWorkPlan(Item):
    grok.implements(ICatalogizationWorkPlan)

    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# catalogization_work_plan_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(ICatalogizationWorkPlan)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
