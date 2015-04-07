# -*- coding: utf-8 -*-
from five import grok
from zope.component import queryUtility, getUtility, getAdapter
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds
from z3c.form import group, field, button

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.supermodel import model

from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable, INamedBlobFileField

from edeposit.content import MessageFactory as _
from z3c.relationfield.schema import RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder, PathSourceBinder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from edeposit.content.aleph_record import IAlephRecord
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from plone.dexterity.utils import createContentInContainer
from plone.dexterity.interfaces import IDexterityFTI
from Acquisition import aq_parent, aq_inner
from plone.rfc822.interfaces import IPrimaryFieldInfo, IPrimaryField
from zope.interface import implements
from zope.component import adapts
from zope.component import getUtility
from zope.schema import getFieldsInOrder
from zope.lifecycleevent import modified
from string import Template
from plone import api
from zope.i18n import translate
from StringIO import StringIO
from subprocess import call
import os.path
from functools import partial
from .changes import IChanges, IApplicableChange
from Acquisition import aq_inner, aq_parent
import simplejson as json
from .tasks import (
    IPloneTaskSender,
    DoActionFor
)

from edeposit.content.amqp_interfaces import (
    IEmailSender
)

def urlCodeIsValid(value):
    return True

from edeposit.content.tasks import (
    IPloneTaskSender,
    CheckUpdates,
)

from edeposit.content.next_step import INextStep

@grok.provider(IContextSourceBinder)
def availableAlephRecords(context):
    path = '/'.join(context.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.alephrecord",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

@grok.provider(IContextSourceBinder)
def availableOriginalFiles(context):
    epublication = aq_parent(aq_inner(context))
    path = '/'.join(epublication.getPhysicalPath())
    query = { "portal_type" : ("edeposit.content.originalfile",),
              "path": {'query' :path } 
             }
    return ObjPathSourceBinder(navigation_tree_query = query).__call__(context)

class IVoucherFileField(INamedBlobFileField):
    pass

class IOriginalFileSourceField(INamedBlobFileField):
    pass

class VoucherFile(NamedBlobFile):
    implements(IVoucherFileField)

class OriginalFileSource(NamedBlobFile):
    implements(IOriginalFileSourceField)

class IOriginalFile(form.Schema, IImageScaleTraversable):
    """
    E-Deposit Original File
    """
    isbn = schema.ASCIILine(
        title=_("ISBN"),
        required = False,
        )

    generated_isbn = schema.Bool(
        title = u"Přidělit ISBN agenturou",
        required = False,
        default = False,
        missing_value = False,
    )

    form.primary('file')
    file = OriginalFileSource (
        title=_(u"Original File of an ePublication"),
        required = False,
        )
    
    # format = schema.ASCIILine (
    #     title=_(u"Format of a file."),
    #     readonly = True,
    #     required = False,
    # )

    # format = schema.Choice(
    #     title=_(u"Format of a file."),
    #     vocabulary="edeposit.content.fileTypes",
    #     required = False,
    # )

    zpracovatel_zaznamu = schema.TextLine(
        title = u'Zpracovatel záznamu',
        required = True,
    )

    url = schema.ASCIILine(
        title=u"URL (pokud je publikace ke stažení z internetu)",
        constraint=urlCodeIsValid,
        required = False,
        )

    related_aleph_record = RelationChoice( title=u"Odpovídající záznam v Alephu",
                                           required = False,
                                           source = availableAlephRecords)
    thumbnail = NamedBlobFile(
        title=_(u"PDF kopie"),
        required = False,
        )

    voucher = VoucherFile (
        title = u"Ohlašovací lístek",
        required = False,
    )

    isClosed= schema.Bool (
        title = _(u'is closed out by Catalogizators'),
        description = u"",
        required = False,
        default = False,
    )

    summary_aleph_record = RelationChoice( title=u"Souborný záznam v Alephu",
                                           required = False,
                                           source = availableAlephRecords )

    primary_originalfile = RelationChoice( title=u"Primární originál",
                                           required = False,
                                           source = availableOriginalFiles)
                                           

@form.default_value(field=IOriginalFile['zpracovatel_zaznamu'])
def zpracovatelDefaultValue(data):
    member = api.user.get_current()
    return member.fullname or member.id

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class OriginalFile(Container):
    grok.implements(IOriginalFile)

    folder_full_view_item_template = Template(u"""
 <div class="item visualIEFloatFix originalfile_folder_full_view_item">
    <h2 class="headline"> <a href="$href" class="summary url $typeClass $stateClass">$title</a> </h2>
    <div class="documentByLine" id="plone-document-byline">
        <span class="ObjectStatus">Stav: <span class="$stateClass">$stateTitle</span></span>
        <span class="documentModified"> <span>Poslední změna:</span>$lastModified</span> </span>
        <span class="documentAuthor"> Ohlásil: <a href="$authorHref">$authorTitle</a></span>
    </div>
</div>
""")

    def hasVoucher(self):
        return bool(self.voucher)

    def folder_full_view_item(self):
        state = api.content.get_state(obj=self)
        creators = self.listCreators()
        mtool = self.portal_membership
        author = creators and creators[0]
        member = api.user.get(username=author)
        plone_utils = self.plone_utils
        stateTitle = translate(self.portal_workflow.getTitleForStateOnType(state, self.portal_type),
                               domain='plone',context = self.REQUEST)
        data = dict(
            href = self.absolute_url(),
            title = self.title,
            typeClass = 'contenttype-' + plone_utils.normalizeString(self.portal_type),
            stateClass = 'state-' + plone_utils.normalizeString(state),
            stateTitle = stateTitle,
            authorHref = author and mtool.getHomeUrl(author),
            authorTitle = member and member.getProperty('fullname') or member.id,
            lastModified = self.toLocalizedTime(self.ModificationDate(),1),
            )
        return OriginalFile.folder_full_view_item_template.substitute(data)

    def updateFormat(self):
        data = self.file and self.file.data
        if data:
            mregistry = api.portal.get_tool('mimetypes_registry')
            mimetype = mregistry.classify(data).normalized()
            self.file.contentType = mimetype
        pass

    def getParentTitle(self):
        return aq_parent(aq_inner(self)).title

    def getNakladatelVydavatel(self):
        return aq_parent(aq_inner(self)).nakladatel_vydavatel

    def getZpracovatelZaznamu(self):
        return self.zpracovatel_zaznamu

    def getPodnazev(self):
        return aq_parent(aq_inner(self)).podnazev

    def getCast(self):
        return aq_parent(aq_inner(self)).cast

    def getNazevCasti(self):
        return aq_parent(aq_inner(self)).nazev_casti

    def needsThumbnailGeneration(self):
        parts = self.file and os.path.splitext(self.file.filename) or None
        isPdf = parts and parts[-1] and 'pdf' in parts[-1].lower()
        return self.file and not isPdf

    def urlToAleph(self):
        record = self.related_aleph_record and getattr(self.related_aleph_record,'to_object',None)
        if not record:
            return ""
        return "http://aleph.nkp.cz/F?func=find-b&find_code=SYS&x=0&y=0&request=%s&filter_code_1=WTP&filter_request_1=&filter_code_2=WLN&adjacent=N" % (record.aleph_sys_number,)

    def urlToAlephMARCXML(self):
        record = self.related_aleph_record and getattr(self.related_aleph_record,'to_object',None)
        if not record:
            return ""
        return "http://aleph.nkp.cz/X?op=find_doc&doc_num=%s&base=nkc" % (record.aleph_sys_number,)

    def urlToKramerius(self):
        return "some"

    def hasSomeAlephRecords(self):
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})
        return len(alephRecords)
        
    # Add your class methods and properties here
    def updateOrAddAlephRecord(self, dataForFactory):
        sysNumber = dataForFactory.get('aleph_sys_number',None)
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})

        # exist some record with the same sysNumber?
        arecordWithTheSameSysNumber = filter(lambda arecord: arecord.aleph_sys_number == sysNumber,
                                             alephRecords)
        print dataForFactory
        if arecordWithTheSameSysNumber:
            print "a record with the same sysnumber"
            # update this record
            alephRecord = arecordWithTheSameSysNumber[0]

            # def isChangedFactory(alephRecord,data):
            #     def isChanged(attr):
            #         return getattr(alephRecord,attr,None) != data.get(attr,None)
            #     return isChanged

            # changedAttrs = filter(isChangedFactory(alephRecord,dataForFactory), dataForFactory.keys())
            # print "changedAttrs", changedAttrs
            # for attr in changedAttrs:
            #     setattr(alephRecord,attr,dataForFactory.get(attr,None))

            changedAttrs = alephRecord.findAndLoadChanges(dataForFactory)
            if changedAttrs and changedAttrs != ['xml']:
                IPloneTaskSender(CheckUpdates(uid=self.UID())).send()

        else:
            createContentInContainer(self, 'edeposit.content.alephrecord', **dataForFactory)

            # if dataForFactory.get('isClosed',False):
            #     self.related_aleph_record = None
            # else:
            #     related_aleph_record = self.related_aleph_record and \
            #                            getattr(self.related_aleph_record,'to_object',None)
            #     if related_aleph_record and not related_aleph_record.isClosed:
            #         self.related_aleph_record = None
                    
            IPloneTaskSender(CheckUpdates(uid=self.UID())).send()


    # Add your class methods and properties here
    def updateOrAddAlephSummaryRecord(self, dataForFactory):
        sysNumber = dataForFactory.get('aleph_sys_number',None)
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})

        # exist some record with the same sysNumber?
        arecordWithTheSameSysNumber = filter(lambda arecord: arecord.aleph_sys_number == sysNumber,
                                             alephRecords)
        print dataForFactory
        if arecordWithTheSameSysNumber:
            print "a record with the same sysnumber"
            # update this record
            alephRecord = arecordWithTheSameSysNumber[0]
            changedAttrs = alephRecord.findAndLoadChanges(dataForFactory)

            # def isChangedFactory(alephRecord,data):
            #     def isChanged(attr):
            #         return getattr(alephRecord,attr,None) != data.get(attr,None)
            #     return isChanged

            # changedAttrs = filter(isChangedFactory(alephRecord,dataForFactory), dataForFactory.keys())
            # print "changedAttrs", changedAttrs
            # for attr in changedAttrs:
            #     setattr(alephRecord,attr,dataForFactory.get(attr,None))

            if changedAttrs and changedAttrs != ['xml']:
                IPloneTaskSender(CheckUpdates(uid=self.UID())).send()

        else:
            createContentInContainer(self, 'edeposit.content.alephrecord', **dataForFactory)

            # if dataForFactory.get('isClosed',False):
            #     self.related_aleph_record = None
            # else:
            #     related_aleph_record = self.related_aleph_record and \
            #                            getattr(self.related_aleph_record,'to_object',None)
            #     if related_aleph_record and not related_aleph_record.isClosed:
            #         self.related_aleph_record = None

            IPloneTaskSender(CheckUpdates(uid=self.UID())).send()

    @property
    def isClosed(self):
        if self.related_aleph_record:
            record = getattr(self.related_aleph_record, 'to_object',None)
            if record:
                return record.isClosed
        return False

    def updateAlephRelatedData(self):
        # try to choose related_aleph_record
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})
        self.related_aleph_record = None
        self.summary_aleph_record = None
        self.primary_originalfile = None

        intids = getUtility(IIntIds)
        if len(alephRecords) == 1:
            self.related_aleph_record = RelationValue(intids.getId(alephRecords[0]))

        if len(alephRecords) > 1:
            isClosedRecords = filter(lambda rr: rr.isClosed, alephRecords)
            if len(isClosedRecords) == 1:
                self.related_aleph_record = RelationValue(intids.getId(isClosedRecords[0]))

            summaryRecords = filter(lambda item: item.isSummaryRecord, alephRecords)
            if summaryRecords:
                self.summary_aleph_record = RelationValue(intids.getId(summaryRecords[0]))
                # TODO
                # doplnil zarazeni primary_originalfile

    def properAlephRecordsChoosen(self):
        # the method says that there is no need to manualy choose
        # related_aleph_record and summary_aleph_record
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})
        if len(alephRecords) == 1:
            return bool(self.related_aleph_record)
        else:
            isClosedRecords = filter(lambda item: item.isClosed, alephRecords)
            summaryRecords = filter(lambda item: item.isSummaryRecord, alephRecords)
            if isClosedRecords:
                if summaryRecords:
                    return bool(self.related_aleph_record) and bool(self.summary_aleph_record)
                else:
                    return bool(self.related_aleph_record)

        return bool(self.related_aleph_record)


    def dataForContributionPDF(self):
        keys = [ii for ii in IOriginalFile.names() if ii not in ('file','thumbnail')]
        return dict(zip(keys,map(partial(getattr,self), keys)))

    def removeInappropriateAlephRecords(self):
        """ remove aleph records that does not refer to this original file """
        alephRecords = self.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})

        def refersToThisOriginalFile(aleph_record):
            absolute_url = self.absolute_url()
            internal_urls = aleph_record.internal_urls
            return (absolute_url in internal_urls)

        toBeRemoved = [rec for rec in alephRecords if not refersToThisOriginalFile(rec)]
        for record in toBeRemoved:
            api.content.delete(obj=record)
        pass

    def checkUpdates(self):
        """ it tries to decide whether some changes appeared in aleph records. 
        The function loads the changes from a proper aleph record into its own attributes.
        The function will plan producent notification.
        """

        # self.removeInappropriateAlephRecords()
        self.updateAlephRelatedData()

        changes = IChanges(self).getChanges()
        for change in changes:
            IApplicableChange(change).apply()

        if changes:
            getAdapter(self, IEmailSender, name="originalfile-has-been-changed").send()
            #self.informProducentAboutChanges = True

        for ii in range(20):
            wasNextState=INextStep(self).doActionFor()
            if not wasNextState:
                break

class OriginalFilePrimaryFieldInfo(object):
    implements(IPrimaryFieldInfo)
    adapts(IOriginalFile)
    
    def __init__(self, context):
        self.context = context
        fti = getUtility(IDexterityFTI, name=context.portal_type)
        self.schema = fti.lookupSchema()
        thumbnail = self.schema['thumbnail']
        if thumbnail.get(self.context):
            self.fieldname = 'thumbnail'
            self.field = thumbnail
        else:
            self.fieldname = 'file'
            self.field = self.schema['file']
    
    @property
    def value(self):
        return self.field.get(self.context)

def tryPrimaryOriginalGetterFactory(getter):
    def tryGetter(self):
        if self.primary_originalfile:
            obj = getattr(self.primary_originalfile,'to_object',None)
            if obj:
                return getter(obj)
        return getter(self)
    return tryGetter

def getAssignedPersonFactory(roleName):
    def getAssignedPerson(self):
        local_roles = self.get_local_roles()
        # print "... get assigned person %s, %s" % (roleName, str(local_roles))
        pairs = filter(lambda pair: roleName in pair[1], local_roles)
        return pairs and pairs[0][0] or None

    return getAssignedPerson

OriginalFile.getAssignedDescriptiveCataloguer = tryPrimaryOriginalGetterFactory(
    getAssignedPersonFactory('E-Deposit: Descriptive Cataloguer')
)

OriginalFile.getAssignedDescriptiveCataloguingReviewer = tryPrimaryOriginalGetterFactory(
    getAssignedPersonFactory('E-Deposit: Descriptive Cataloguing Reviewer')
)

OriginalFile.getAssignedSubjectCataloguer = tryPrimaryOriginalGetterFactory(
    getAssignedPersonFactory('E-Deposit: Subject Cataloguer')
)

OriginalFile.getAssignedSubjectCataloguingReviewer = tryPrimaryOriginalGetterFactory(
    getAssignedPersonFactory('E-Deposit: Subject Cataloguing Reviewer')
)

class ThumbnailView(grok.View):
    grok.context(IOriginalFile)
    grok.require('zope2.View')
    grok.name("thumbnail")

    def __call__(self):
        thumbnail = self.context.thumbnail
        url = thumbnail and "/".join(thumbnail.getPhysicalPath()) \
            or "/".join(self.context.getPhysicalPath() + ("documentviewer",))
        self.request.response.redirect(url)


import plone.namedfile

# class folder_full_view_item(grok.View):
#     grok.context(IOriginalFile)
#     grok.require('zope2.View')
#     grok.name('folder_full_view_item')
    
class Download(plone.namedfile.browser.Download):
    pass

class DisplayFile(plone.namedfile.browser.DisplayFile):
    pass

class HasVoucherView(grok.View):
    grok.context(IOriginalFile)
    grok.require('zope2.View')
    grok.name('has-voucher')
    
    def render(self):
        return json.dumps(dict(hasVoucher = bool(self.context.voucher)))


class IChangeSourceForm(form.Schema):
    file = NamedBlobFile(
        title=u"Připojit soubor s ePublikací",
        required = False,
        )
    
class ChangeSourceView(form.SchemaForm):
    grok.context(IOriginalFile)
    grok.require('cmf.ModifyPortalContent')
    grok.name('change-source')

    schema = IChangeSourceForm
    ignoreContext = False
    enable_form_tabbing = False
    autoGroups = False
    template = ViewPageTemplateFile('originalfile_templates/changesource.pt')
    prefix = 'sourceform'

    @button.buttonAndHandler(u"Odeslat", name="save")
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        self.context.file = data['file']
        wft = api.portal.get_tool('portal_workflow')
        if self.context.file:
            wft.doActionFor(self.context, (self.context.isbn and 'submitDeclarationToISBNValidation')
                            or ('submitDeclarationToAntivirus'))
        self.request.response.redirect(self.context.absolute_url())


class OriginalFileChangeSource(object):
    implements(IChangeSourceForm)
    adapts(IOriginalFile)

    def __init__(self, context):
        self.context = context
    
    @property
    def file(self):
        return self.context.file

