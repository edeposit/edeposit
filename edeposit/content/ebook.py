from five import grok
from zope import schema
from plone.directives import form

import re

from zope.interface import Invalid

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from edeposit.content import EDepositMessageFactory as _

from plone.namedfile import field

# Uniqueness validator
from z3c.form import validator
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName

# View
from zope.component import getMultiAdapter
from plone.memoize.instance import memoize

def isbnCodeIsValid(value):
    """Contraint function to make sure the given isbn code is valid
    """
    return True

def isYear(value):
    """Contraint function to validate year value
    """
    if not re.match("^[0-9]*$",value):
        raise Invalid(_(u"This does not look like a year"))
    return True

class IEBook(form.Schema):
    """E-Book informations for manual acquisition
    """
    
    title = schema.TextLine(
        title=_(u"Title"),
        description=_(u"Please enter a title of an ebook"),
    )

    ISBN = schema.ASCIILine(
        title=_(u"ISBN code"),
        description=_(u"Code used for unique identification in Czech libraries"),
        constraint=isbnCodeIsValid,
    )
    
    part = schema.TextLine(
        title=_(u"Part"),
        description=_(u"Please enter a name of a part"),
    )

    ebookFormat = schema.TextLine(
        title=_(u"EBook format"),
        description=_(u"Please enter a format of an ebook"),
    )

    published = schema.TextLine (
        title=_(u"Year of publishing"),
        description=_(u"Please enter a format of an ebook"),
        constraint=isYear,
    )

    publishedTogetherWith = schema.TextLine(
        title=_(u"Published together with"),
        description=_(u"Please enter a name of a ebook that was published with"),
    )

    ebook = field.NamedBlobFile(title=u"EBook file")
 
    # highlightedFilms = RelationList(
    #         title=_(u"Highlighted films"),
    #         description=_(u"Films to highlight for this cinema"),
    #         value_type=RelationChoice(
    #                 source=ObjPathSourceBinder(
    #                         object_provides=IFilm.__identifier__
    #                     ),
    #             ),
    #         required=False,
    #     )

# class ValidateCinemaCodeUniqueness(validator.SimpleFieldValidator):
#     """Validate site-wide uniquneess of cinema codes.
#     """
    
#     def validate(self, value):
#         # Perform the standard validation first
#         super(ValidateCinemaCodeUniqueness, self).validate(value)
        
#         if value is not None:
#             catalog = getToolByName(self.context, 'portal_catalog')
#             results = catalog({'cinemaCode': value,
#                                'object_provides': ICinema.__identifier__})
            
#             contextUUID = IUUID(self.context, None)
#             for result in results:
#                 if result.UID != contextUUID:
#                     raise Invalid(_(u"The cinema code is already in use"))

# validator.WidgetValidatorDiscriminators(
#         ValidateCinemaCodeUniqueness,
#         field=ICinema['cinemaCode'],
#     )
# grok.global_adapter(ValidateCinemaCodeUniqueness)

class View(grok.View):
    """Default view (called "@@view"") for a cinema.
    
    The associated template is found in ebook_templates/view.pt.
    """
    
    grok.context(IEBook)
    grok.require('zope2.View')
    grok.name('view')
    
    def update(self):
        #self.haveHighlightedFilms = len(self.highlightedFilms()) > 0
        pass

    # @memoize
    # def highlightedFilms(self):
        
    #     films = []
        
    #     if self.context.highlightedFilms is not None:
    #         for ref in self.context.highlightedFilms:
    #             obj = ref.to_object
            
    #             scales = getMultiAdapter((obj, self.request), name='images')
    #             scale = scales.scale('image', scale='thumb')
    #             imageTag = None
    #             if scale is not None:
    #                 imageTag = scale.tag()
            
    #             films.append({
    #                     'url': obj.absolute_url(),
    #                     'title': obj.title,
    #                     'summary': obj.description,
    #                     'imageTag': imageTag,
    #                 })
        
    #     return films
