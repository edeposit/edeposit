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
            mregistry = api.portal.get_tool('mimetypes_registry')
            data = self.context.file.data
            return mregistry.classify(data).normalized()
        return 'text/html'

    # @property
    # def tags(self):
    #     return set(self.context.Subject())

    # @tags.setter
    # def tags(self, value):
    #     if value is None:
    #         value = ()
    #     self.context.setSubject(tuple(value))

alsoProvides(IFormat, IFormFieldProvider)
