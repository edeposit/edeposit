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


from edeposit.content import MessageFactory as _


# Interface class; used to define content-type schema.

class IOriginalFileContributingRequest(form.Schema, IImageScaleTraversable):
    """
    Description of the Example Type
    """
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        description=_(u"Value of ISBN"),
        required = True,
        )
    choosen_aleph_sys_number = schema.ASCIILine (
        title = _(u'Aleph SysNumber to load this document for'),
        description = _(u'Internal SysNumber of a record in Aleph to load this document for.'),
        required = False,
    )
    choosen_aleph_library = schema.ASCIILine (
        title = _(u'Aleph Library to load this document for'),
        description = _(u'Library of a record in Aleph to load this document for.'),
        required = False,
    )

    

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

class SampleView(grok.View):
    """ sample view class """

    grok.context(IOriginalFileContributingRequest)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
