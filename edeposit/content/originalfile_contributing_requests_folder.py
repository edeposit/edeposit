# -*- coding: utf-8 -*-
from five import grok
import zope

from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from .originalfile_contributing_request import IOriginalFileContributingRequest
from edeposit.content import MessageFactory as _
from edeposit.content.utils import is_valid_isbn
from z3c.form.interfaces import WidgetActionExecutionError, ActionExecutionError, IObjectFactory, IValidator, IErrorViewSnippet

# Interface class; used to define content-type schema.

class IOriginalFileContributingRequestsFolder(form.Schema, IImageScaleTraversable):
    """
    Folder for original file contributing requests
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/originalfile_contributing_requests_folder.xml to define the content type.

    form.model("models/originalfile_contributing_requests_folder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class OriginalFileContributingRequestsFolder(Container):
    grok.implements(IOriginalFileContributingRequestsFolder)
    # Add your class methods and properties here
    pass


# View class
# The view will automatically use a similarly named template in
# originalfile_contributing_requests_folder_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.


class ContributeForm(form.Form):
    grok.context(IOriginalFileContributingRequestsFolder)
    grok.name('contribute')
    grok.require('zope2.View')

    fields = field.Fields(IOriginalFileContributingRequest)

    label = _(u"Odevzdání dokumentu")
    description = _(u"Známe ISBN záznamu v Alephu, chceme k němu odevzdat odpovídající dokument.")
    ignoreContext = True

    def update(self):
        self.request.set('disable_border', True)
        return super(ContributeForm, self).update()

    def extractData(self):
        def getErrorView(widget,error):
            view = zope.component.getMultiAdapter( (error, 
                                                    self.request, 
                                                    widget, 
                                                    widget.field, 
                                                    widget.form, 
                                                    self.context), 
                                                   IErrorViewSnippet)
            view.update()
            widget.error = view
            return view

        data, errors = super(ContributeForm,self).extractData()
        isbn = data.get('isbn',None)
        print 'isbn: ', isbn
        if isbn:
            print "isbn appeared: ", isbn
            isbnWidget = self.widgets.get('isbn',None)
            valid = is_valid_isbn(isbn)
            if not valid:
                # validity error
                print "isbn is not valid"
                errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'chyba v isbn')),)
                pass
            else:
                try:
                    appearedAtAleph = edeposit.amqp.aleph.aleph.getISBNCount(isbn)
                    if not appearedAtAleph:
                        errors += (getErrorView(isbnWidget, zope.interface.Invalid(u'isbn nemá v Alephu záznam. Použijte jíné.')),)
                except:
                    pass

        return (data,errors)




    @button.buttonAndHandler(u"Načíst záznam z Alephu")
    def contribute(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        data['title'] = u"Žádost na odevzdání dokumentu"
        newObject = createContentInContainer(self.context,'edeposit.content.originalfilecontributingrequest',**data)
        self.request.response.redirect(newObject.absolute_url())
        pass
