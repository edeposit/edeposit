# -*- coding: utf-8 -*-
from five import grok

from z3c.form import group, field, button
from zope import schema
from zope.interface import invariant, Invalid, Interface
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable
from Acquisition import aq_inner, aq_parent
from zope.globalrequest import getRequest
from plone import api
from edeposit.content import MessageFactory as _
from z3c.form.form import extends

from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

# Interface class; used to define content-type schema.

class IePublicationFolder(form.Schema, IImageScaleTraversable):
    """
    E-Deposit ePublication Folder
    """

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/epublicationfolder.xml to define the content type.

    form.model("models/epublicationfolder.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class ePublicationFolder(Container):
    grok.implements(IePublicationFolder)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# epublicationfolder_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    """ sample view class """

    grok.context(IePublicationFolder)
    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here


@grok.provider(IContextSourceBinder)
def selectedEPublications(context):
    request = getRequest()
    selected_paths = request.form['paths']
    pcatalog = api.portal.get_tool('portal_catalog')
    parentPath = context.absolute_url_path()
    query=dict(portal_type = 'edeposit.content.epublication',
               path = filter(lambda path: path.index(parentPath)==0, selected_paths)
           )
    brains = pcatalog(query)
    import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
    terms = map(lambda item: SimpleVocabulary.createTerm(item, item['id'], item['id']),  brains)
    return SimpleVocabulary(terms)

@grok.provider(IContextSourceBinder)
def availableProducentWorkers(context):
    administrators = aq_parent(aq_inner(context))['producent-administrators']
    terms = map(lambda admin: SimpleVocabulary.createTerm(admin, admin.title, admin.title), administrators)
    return SimpleVocabulary(terms)


class IEPublicationsTableRow(form.Schema):
    def getNazev(self):
        return self.title

    podnazev = schema.TextLine (
        title = u"Podnázev",
        required = False,
    )

    pass

class IFormSchema(Interface):
    four = schema.TextLine(title=u"Four")
    table = schema.List(title=u"Table",
                        value_type=DictRow(title=u"tablerow", schema=IEPublicationsTableRow))
    
class EPublicationsTableForm(form.EditForm):
    extends(form.EditForm)
    grok.name('grid_view')
    grok.require('zope2.View')
    grok.context(IePublicationFolder)
    fields = field.Fields(IFormSchema)
        
    
# class IAssignWorkerForm(form.Schema):
#     selectedEPublications = schema.List(
#         title = u"Selected EPublications",
#         required = False,
#         value_type = schema.Choice(source = selectedEPublications)
#     )
#     asignedWorker = schema.Choice (
#         title = u"Assigned worker",
#         source = availableProducentWorkers,
#         required = False
#     )
    

# class AssignWorkerForm(form.SchemaForm):
#     grok.name('assign_worker')
#     grok.require('zope2.View')
#     grok.context(IePublicationFolder)

#     schema = IAssignWorkerForm
#     ignoreContext = True

#     label = u"You can assign worker for those ePublications"
#     description = u"Assign a worker"

#     # @button.buttonAndHandler(u'Potvrdit')
#     # def handleSubmit(self, action):
#     #     data, errors = self.extractData()
#     #     if errors:
#     #         self.status = self.formErrorsMessage
#     #         return

#     #     # Do something with valid data here

#     #     # Set status on this form page
#     #     # (this status message is not bind to the session and does not go thru redirects)
#     #     self.status = "Thank you very much!"
#     #     pass

    
