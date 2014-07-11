# -*- coding: utf-8 -*-
from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
import simplejson as json
from plone import api
from edeposit.content import MessageFactory as _
from .aleph_record import IAlephRecord

from z3c.relationfield.schema import RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder

# Interface class; used to define content-type schema.

@grok.provider(IContextSourceBinder)
def availableAlephRecords(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.alephrecord",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

class IOriginalFileContributingRequest(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = True,
        )
    choosen_aleph_record = RelationChoice( title=u"Odpovídající záznam v Alephu",
                                           required = False,
                                           source = availableAlephRecords)
    

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class OriginalFileContributingRequest(Container):
    grok.implements(IOriginalFileContributingRequest)
    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# originalfile_contributing_request_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class StateView(grok.View):
    """ sample view class """

    grok.context(IOriginalFileContributingRequest)
    grok.require('zope2.View')
    grok.name('state')

    def render(self):
        data = {'state': api.content.get_state(obj=self.context),
                'choosen_aleph_record': self.context.choosen_aleph_record \
                and self.context.choosen_aleph_record.to_path or "",
                'relatedItems': map(lambda item: {
                    'to_path': item.to_path,
                    'to_object': str(item.to_object),
                }, self.context.relatedItems),
        }
        self.request.response.setHeader("Content-type", "application/json")
        return json.dumps(data, sort_keys=True)
