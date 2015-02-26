# -*- coding: utf-8 -*-
from zope.component import queryUtility, getUtility, getMultiAdapter
from zope.container.interfaces import (
    IObjectAddedEvent, 
    IObjectRemovedEvent,
    IContainerModifiedEvent
)
from zope.lifecycleevent import modified
from z3c.relationfield import RelationValue
from zope.app.intid.interfaces import IIntIds

import re
from logging import getLogger
from decimal import Decimal
logger = getLogger('edeposit.content.handlers')

from plone.dexterity.utils import createContentInContainer

from zope.interface import Interface, Attribute, implements, classImplements

from plone import api
from edeposit.content import MessageFactory as _
from Acquisition import aq_inner, aq_parent

from five import grok
from datetime import datetime

from edeposit.amqp.serializers import (
    serialize,
    deserialize
)

from edeposit.content.amqp import (
    IAMQPHandler,
    IAMQPSender,
    parse_headers,
    make_headers,
    AlephSearchDocumentResult,
    AlephSearchSummaryRecordResult,
)
import json

from collections import namedtuple

from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer
from collective.zamqp.connection import BlockingChannel
from collective.zamqp.interfaces import IMessageArrivedEvent
from edeposit.amqp.aleph.datastructures.epublication import (
    EPublication,
    Author
)

from edeposit.amqp.aleph.datastructures.semanticinfo import (
    SemanticInfo
)

from edeposit.amqp.aleph.datastructures.alephrecord import (
    AlephRecord
)

from edeposit.amqp.aleph.datastructures.results import (
    ISBNValidationResult,
    CountResult,
    SearchResult,
    ExportResult,
)

from edeposit.amqp.antivirus.structures import (
    ScanResult,
    ScanFile
)

from edeposit.amqp.calibre.structures import (
    ConversionRequest,
    ConversionResponse,
)

from edeposit.amqp.pdfgen.structures import (
    PDF
)

from edeposit.content.tasks import *

class IAMQPError(Interface):
    payload = Attribute("")
    exception_name = Attribute("")
    exception = Attribute("")
    headers = Attribute("")

class AMQPError(namedtuple('AMQPError',IAMQPError.names())):
    implements(IAMQPError)
    pass

class ISBNValidateRequestProducent(Producer):
    grok.name('amqp.isbn-validate-request')

    connection_id = "aleph"
    exchange = "validate"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass

class ISBNCountRequestProducent(Producer):
    grok.name('amqp.isbn-count-request')

    connection_id = "aleph"
    exchange = "count"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass

class IAlephResponse(Interface):
    """Message marker interface"""

class AlephResponseConsumer(Consumer):
    grok.name('amqp.aleph-response-consumer')
    connection_id = "aleph"
    queue = "plone"
    serializer = "plain"
    marker = IAlephResponse
    pass

@grok.subscribe(IAlephResponse, IMessageArrivedEvent)
def handleAlephResponse(message, event):
    print "handle aleph response"
    wft = api.portal.get_tool('portal_workflow')
    headers = message.header_frame.headers
    (context, session_data) = parse_headers(headers)
    if not context:
        print "no context at headers"
        print message.body
        message.ack()
        return

    if "exception" in headers:
        amqpError = AMQPError(payload=message.body, 
                              exception_name = headers.get('exception_name'),
                              exception = headers.get('exception'),
                              headers = headers)
        getMultiAdapter((context,amqpError),IAMQPHandler).handle()
        message.ack()
    else:
        result = deserialize(json.dumps(message.body),globals())
        dataKeys = session_data.keys()
        ResultFactory = None
        if 'renew-records-for-sysnumber' in dataKeys:
            ResultFactory = AlephSearchDocumentResult
        elif 'load-summary-record-for-sysnumber' in dataKeys:
            ResultFactory = AlephSearchSummaryRecordResult

        if ResultFactory:
            records = result.records
            if records:
                newResult = ResultFactory(record = result.records[0])
                getMultiAdapter((context,newResult),IAMQPHandler).handle()
            else:
                print "... there are no records at the result"
        else:
            getMultiAdapter((context,result),IAMQPHandler).handle()

        message.ack()

class IAntivirusResponse(Interface):
    """Message marker interface"""

class AntivirusResponseConsumer(Consumer):
    grok.name('amqp.antivirus-response-consumer')
    connection_id = "antivirus"
    queue = "plone"
    serializer = "plain"
    marker = IAntivirusResponse
    pass

@grok.subscribe(IAntivirusResponse, IMessageArrivedEvent)
def handleAntivirusResponse(message, event):
    print "handle antivirus response"
    wft = api.portal.get_tool('portal_workflow')
    headers = message.header_frame.headers
    (context, session_data) = parse_headers(headers)
    if not context:
        print "no context at headers"
        print message.body
        message.ack()
        return

    if "exception" in headers:
        amqpError = AMQPError(payload=message.body, 
                              exception_name = headers.get('exception_name'),
                              exception = headers.get('exception'),
                              headers = headers)
        getMultiAdapter((context,amqpError),IAMQPHandler).handle()
        message.ack()
    else:
        # Messages from Antivir has its own deserialization logic. 
        # So we will use it.
        result = deserialize(json.dumps(message.body),globals())
        getMultiAdapter((context,result),IAMQPHandler).handle()
        message.ack()
    pass

class ICalibreResponse(Interface):
    """Message marker interface"""

class CalibreResponseConsumer(Consumer):
    grok.name('amqp.calibre-response-consumer')
    connection_id = "calibre"
    queue = "plone"
    serializer = "plain"
    marker = ICalibreResponse
    pass

@grok.subscribe(ICalibreResponse, IMessageArrivedEvent)
def handleCalibreResponse(message, event):
    print "handle calibre response"
    wft = api.portal.get_tool('portal_workflow')
    headers = message.header_frame.headers
    (context, session_data) = parse_headers(headers)
    if not context:
        print "no context at headers"
        message.ack()
        return

    if "exception" in headers:
        amqpError = AMQPError(payload=message.body, 
                              exception_name = headers.get('exception_name'),
                              exception = headers.get('exception'),
                              headers = headers)
        getMultiAdapter((context,amqpError),IAMQPHandler).handle()
        message.ack()
    else:
        result = deserialize(json.dumps(message.body),globals())
        getMultiAdapter((context,result),IAMQPHandler).handle()
        message.ack()

class IPDFGenResponse(Interface):
    """Message marker interface"""

class PDFGenResponseConsumer(Consumer):
    grok.name('amqp.pdfgen-response-consumer')
    connection_id = "pdfgen"
    queue = "plone"
    serializer = "plain"
    marker = IPDFGenResponse
    pass

@grok.subscribe(IPDFGenResponse, IMessageArrivedEvent)
def handlePDFGenResponse(message, event):
    print "handle pdfgen response"
    wft = api.portal.get_tool('portal_workflow')
    headers = message.header_frame.headers
    (context, session_data) = parse_headers(headers)
    if not context:
        print "no context at headers"
        message.ack()
        return

    if "exception" in headers:
        amqpError = AMQPError(payload=message.body, 
                              exception_name = headers.get('exception_name'),
                              exception = headers.get('exception'),
                              headers = headers)
        getMultiAdapter((context,amqpError),IAMQPHandler).handle()
        message.ack()
    else:
        result = deserialize(json.dumps(message.body),globals())
        getMultiAdapter((context,result),IAMQPHandler).handle()
        message.ack()

class IPloneTask(Interface):
    """Message marker interface"""

class PloneTaskConsumer(Consumer):
    grok.name('amqp.plone-task-consumer')
    connection_id = "plone"
    queue = "plone"
    serializer = "plain"
    marker = IPloneTask
    pass

@grok.subscribe(IPloneTask, IMessageArrivedEvent)
def handlePloneTask(message, event):
    headers = message.header_frame.headers or {}
    (context, session_data) = parse_headers(headers)
    if not context:
        # we will attach default context of an amqp message:
        # amqp folder.
        print "... no context at headers so try AMQP Folder as default context"
        pcatalog = api.portal.get_tool('portal_catalog') 
        context = pcatalog(portal_type="edeposit.content.amqpfolder")[0].getObject()
        session_data={}

    if "exception" in headers:
        amqpError = AMQPError(payload=message.body, 
                              exception_name = headers.get('exception_name'),
                              exception = headers.get('exception'),
                              headers = headers)
        getMultiAdapter((context,amqpError),IAMQPHandler).handle()
        message.ack()
    else:
        result = deserialize(message._serialized_body,globals())
        getMultiAdapter((context,result),IAMQPHandler).handle()
        message.ack()


# when ePublication is added
def added(context,event):
    """When an object is added, create collection for simple list of authors
    """
    context.invokeFactory('Collection','authors',
                          title=_(u"Review of authors"),
                          query=[{'i': 'portal_type',
                                  'o': 'plone.app.querystring.operation.selection.is',
                                  'v': ['edeposit.content.author',]},
                                 {'i': 'path', 
                                  'o': 'plone.app.querystring.operation.string.relativePath', 
                                  'v': '../'}
                                 ]
                          )
    context.invokeFactory('Collection','original-files', 
                          title="Soubory s originály",
                          query=[{'i': 'portal_type', 
                                  'o': 'plone.app.querystring.operation.selection.is', 
                                  'v': ['edeposit.content.originalfile',]
                                  },
                                 {'i': 'path', 
                                  'o': 'plone.app.querystring.operation.string.relativePath', 
                                  'v': '../'}
                                 ],
                          )
    pass

def addedEPublicationFolder(context, event):
    def queryForStates(*args):
        return [ {'i': 'portal_type',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': ['edeposit.content.epublication']},
                 {'i': 'review_state',
                  'o': 'plone.app.querystring.operation.selection.is',
                  'v': args},
                 {'i': 'path', 
                  'o': 'plone.app.querystring.operation.string.relativePath', 
                  'v': '../'}
                 ]
    portal = api.portal.get()
    collections = [ dict( contexts=[context],
                          name = "ePublications-in-declarating",
                          title=_(u"ePublications in declaring"),
                          query= queryForStates('declaration')
                          ),
                    dict( contexts=[context],
                          name = "ePublications-waiting-for-approving",
                          title = _(u"ePublications waiting for preparing of acquisition"),
                          query= queryForStates('waitingForApproving')
                          ),
                    dict( contexts=[context],
                          name  = "ePublications-with-errors",
                          title = _(u"ePublications with errors"),
                          query = queryForStates('declarationWithError')
                          ),
                    dict( contexts=[context],
                          name = "ePublications-for-RIV-review",
                          title = _(u"ePublications waiting for RIV to be reviewed"),
                          query = [
                              {'i': 'portal_type',
                               'o': 'plone.app.querystring.operation.selection.is',
                               'v': ['edeposit.content.epublication']},
                              {'i':'offerToRIV',
                               'o': 'plone.app.querystring.operation.selection.is',
                               'v': [True]},
                          ]
                      )
                    ]
    return
    for collection in collections:
        for folder in collection['contexts']:
            name = collection['name']
            name in folder.keys() or \
                folder.invokeFactory('Collection', name,
                                     title=collection['title'],
                                     query=collection['query'],
                                     )
            
    
def addedISBNCountRequest(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    isbnq = ISBNQuery(context.isbn)
    request = CountRequest(isbnq)
    producer = getUtility(IProducer, name="amqp.isbn-count-request")
    producer.publish(serialize(request),
                     content_type = 'application/json',
                     headers = {'UUID': json.dumps({'request_UID': str(context.UID()),
                                                    'systemMessages_UID': str(systemMessages.UID())
                                                })
                            }
                 )
    context.sent = datetime.now()
    wft.doActionFor(epublication, 'notifySystemAction', comment=context.title)
    return

def addedISBNValidateRequest(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    request = ISBNValidationRequest(context.isbn)
    producer = getUtility(IProducer, name="amqp.isbn-validate-request")
    producer.publish(serialize(request),
                     content_type = 'application/json',
                     headers = {'UUID': json.dumps({'request_UID': str(context.UID()),
                                                    'systemMessages_UID': str(systemMessages.UID())
                                                })
                            }
                 )
    context.sent = datetime.now()
    wft.doActionFor(epublication, 'notifySystemAction', comment=context.title)
    return

def addedISBNCountResult(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    wft.doActionFor(epublication, 'notifySystemAction', comment=context.title)
    pass

def addedISBNValidateResult(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    wft.doActionFor(epublication, 'notifySystemAction', comment=context.title)
    pass

def addedAlephException(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    wft.doActionFor(epublication, 'alephException', comment=context.title)
    pass

class AlephExportRequestProducent(Producer):
    grok.name('amqp.aleph-export-request')

    connection_id = "aleph"
    exchange = "export"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass


def addedAlephExportRequest(context, event):
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    originalFile = epublication[context.originalFileID]
    authors = map(lambda aa: Author(lastName = aa.fullname, firstName="", title = ""), epublication.authors.results())
    epublicationRecord =  EPublication (
        ISBN = originalFile.isbn or "",
        nazev = epublication.title or "",
        podnazev = epublication.podnazev or "",
        vazba = "online",
        cena = str(epublication.cena or ""),
        castDil = epublication.cast or "",
        nazevCasti = epublication.nazev_casti or "",
        nakladatelVydavatel = epublication.nakladatel_vydavatel or "",
        datumVydani = str(epublication.rok_vydani),
        poradiVydani = epublication.poradi_vydani or "",
        zpracovatelZaznamu = originalFile.zpracovatel_zaznamu or "",
        format = originalFile.format or "",
        url = originalFile.url or "",
        mistoVydani = epublication.misto_vydani,
        ISBNSouboruPublikaci = epublication.isbn_souboru_publikaci or "",
        autori = map(lambda author: author.lastName, filter(lambda author: author.lastName, authors)),
        originaly = [],
        internal_url = originalFile.absolute_url() or "",
    )

    request = ExportRequest(epublication=epublicationRecord)
    producer = getUtility(IProducer, name="amqp.aleph-export-request")
    producer.publish(serialize(request),
                     content_type = 'application/json',
                     headers = {'UUID': json.dumps({'request_UID': str(context.UID()),
                                                    'systemMessages_UID': str(systemMessages.UID())
                                                })
                            }
                 )
    context.sent = datetime.now()
    wft.doActionFor(epublication, 'exportToAlephSubmitted')
    return

# def addedAlephExportResult(context, event):
#     logger.debug('added aleph export result')
#     wft = api.portal.get_tool('portal_workflow')
#     systemMessages = event.newParent
#     epublication = aq_parent(aq_inner(systemMessages))
#     print "added aleph export result"
#     wft.doActionFor(epublication, 'exportToAlephOK')
#     return

def addedOriginalFile(context, event):
    # find related epublication
    epublication = aq_parent(aq_inner(context))
    print "addedOriginalFile", str(epublication)
    logger.debug('addedOriginalFile: ' + str(epublication))
    intids = getUtility(IIntIds)
    context.relatedItems = [RelationValue(intids.getId(epublication))]
    pass

def addedAlephRecord(context, event):
    originalfile = aq_parent(aq_inner(context))
    originalfile.updateAlephRelatedData()

def updateFormat(context, event):
    originalfile = aq_inner(context)
    originalfile.updateFormat()
    
# class HandlerError(Exception):
#     pass

# def getContentIfKeyExists(keyName,key):
#     if key.get(keyName,None):
#         return api.content.get(UID=key[keyName])
#     return None

# def handleISBNValidationResult(uuid, data):
#     wft = api.portal.get_tool('portal_workflow')
#     keyContent = json.loads(uuid)
#     print "key contents of: " , keyContent
#     uuidType  = keyContent.get('type',None)
#     uuidValue = keyContent.get('value', None)
#     if (not uuidType or not uuidValue):
#         raise HandlerError("no system message or no request message exists in key")
#     context = getContentIfKeyExists('context_UID',uuidValue)
#     if not context:
#         raise HandlerError("chyba: toto uuid neexistuje: " + str(uuid))
#     if uuidType == 'edeposit.originalfile-isbn-validation':
#         pass
    
# def handleSearchResult(uuid, data):
#     wft = api.portal.get_tool('portal_workflow')
#     keyContent = json.loads(uuid)
#     print "key contents of: " , keyContent
#     uuidType  = keyContent.get('type',None)
#     uuidValue = keyContent.get('value', None)
#     if (not uuidType or not uuidValue):
#         raise HandlerError("no system message or no request message exists in key")

#     context = getContentIfKeyExists('context_UID',uuidValue)
#     if not context:
#         raise HandlerError("chyba: toto uuid neexistuje: " + str(uuid))
#     if uuidType == 'edeposit.originalfile-load-epublication-request':
#         with api.env.adopt_user(username="system"):
#             producent = aq_parent(aq_parent(context))
#             ePublicationsFolder = producent['epublications']
#             for record in data.records:
#                 epublication = record.epublication
#                 result = re.search('([0-9]+[\.,]{0,1}[0-9]*)',epublication.cena)
#                 price = (result and result.group(0) or "").replace(",",".")
#                 dataForFactory = {
#                     'title': str(epublication.nazev),
#                     'podnazev': epublication.podnazev,
#                     'cena': price and Decimal(price),
#                     'isbn_souboru_publikaci': epublication.ISBNSouboruPublikaci,
#                     'cast': epublication.castDil,
#                     'nazev_casti': epublication.nazevCasti,
#                     'nakladatel_vydavatel': epublication.nakladatelVydavatel,
#                     'rok_vydani':  int(epublication.datumVydani),
#                     'poradi_vydani': epublication.poradiVydani,
#                     'misto_vydani': epublication.mistoVydani,
#                     'vydano_v_koedici_s': "",  # TODO
#                     'zpracovatel_zaznamu': epublication.zpracovatelZaznamu,
#                 }
#                 newEPublication = createContentInContainer(ePublicationsFolder,
#                                                      'edeposit.content.epublication',
#                                                      **dataForFactory
#                                                  )
#                 # TODO: nacteni autoru
#                 for author in epublication.autori:
#                     pass

#                 # vytvoreni predpripraveneho originalFile
#                 # doplneni relationItems v zadosti
#                 dataForOriginalFile = {
#                     'title': epublication.nazev + u' - originál',
#                     'isbn': epublication.ISBN[0],
#                     'generated_isbn': False,
#                 }
#                 newOriginalFile = createContentInContainer( 
#                     newEPublication,
#                     'edeposit.content.originalfile',
#                     **dataForOriginalFile
#                 )
#                 # ulozeni odkazu na aleph record do original file
#                 intids = getUtility(IIntIds)

#                 # aleph record zkopirujeme do original file
#                 # bude jednodussi prace s vyberem primarniho aleph
#                 # zaznamu
#                 newAlephRecord = api.content.copy(context.choosen_aleph_record.to_object, newOriginalFile)
#                 newOriginalFile.related_aleph_record = RelationValue(intids.getId(newAlephRecord))
#                 newOriginalFile.relatedItems = [
#                     RelationValue(intids.getId(newEPublication)),
#                     RelationValue(intids.getId(context)),
#                 ]

#                 context.relatedItems = [ 
#                     RelationValue(intids.getId(newEPublication)),
#                     RelationValue(intids.getId(newOriginalFile))
#                 ]
#                 wft.doActionFor(newEPublication,'loadedFromAleph')
#                 wft.doActionFor(context, 'ePublicationWasLoadedFromAleph')
#             pass
#         pass
#     elif uuidType == 'edeposit.originalfile-search-alephrecords-request':
#         with api.env.adopt_user(username="system"):
#             for record in data.records:
#                 epublication = record.epublication
#                 dataForFactory = {
#                     'title': "".join([u"Záznam v Alephu: ",
#                                       str(epublication.nazev), 
#                                       '(', 
#                                       str(record.docNumber),
#                                       ')']),
#                     'nazev':  str(epublication.nazev),
#                     'isbn': epublication.ISBN[0],
#                     'podnazev': epublication.podnazev,
#                     'cast': epublication.castDil,
#                     'nazev_casti': epublication.nazevCasti,
#                     'rok_vydani': epublication.datumVydani,
#                     'aleph_sys_number': record.docNumber,
#                     'aleph_library': record.library,
#                 }
#                 createContentInContainer(context,'edeposit.content.alephrecord',
#                                          **dataForFactory
#                                      )
#                 pass
#             modified(context)
#             wft.doActionFor(context, 'gotAlephRecords')
#         pass
#     elif uuidType == 'edeposit.epublication-load-aleph-records':
#         with api.env.adopt_user(username="system"):
#             for record in data.records:
#                 epublication = record.epublication
#                 isbn = epublication.ISBN[0]
#                 dataForFactory = {
#                     'title': "".join([u"Záznam v Alephu: ",
#                                       str(epublication.nazev), 
#                                       '(', str(record.docNumber), ')']),
#                     'nazev':  str(epublication.nazev),
#                     'isbn': isbn,
#                     'podnazev': epublication.podnazev,
#                     'cast': epublication.castDil,
#                     'nazev_casti': epublication.nazevCasti,
#                     'rok_vydani': epublication.datumVydani,
#                     'aleph_sys_number': record.docNumber,
#                     'aleph_library': record.library,
#                 }
#                 context.updateOrAddAlephRecord(dataForFactory)
#             pass
#     else:
#         raise HandlerError('wrong type of uuid: ' + uuidType)
    

# @grok.subscribe(IAlephResponse, IMessageArrivedEvent)
# def handleAlephResponse(message, event):
#     print "handle aleph response"
#     wft = api.portal.get_tool('portal_workflow')
#     headers = message.header_frame.headers
#     key=headers.get('UUID',None)
#     if not key:
#         print "no UUID at headers"
#         print message.body
#         message.ack()
#         return

#     def getContentIfKeyExists(keyName,key):
#         if key.get(keyName,None):
#             return api.content.get(UID=key[keyName])
#         return None

#     keyContent = json.loads(key)
#     print "key contents of: " , keyContent
#     uuidType  = keyContent.get('type',None)
#     uuidValue = keyContent.get('value', None)
#     if (not uuidType or not uuidValue):
#         print "wrong key", key
#         message.ack()
#         return

#     # Messages from Aleph has its own deserialization logic. 
#     # So we will use it.
#     data = deserialize(json.dumps(message.body),globals())
#     if isinstance(data, SearchResult):
#         try:
#             handleSearchResult(key, data)
#         except HandlerError,e:
#             print str(e)
#             pass
#         message.ack()            
#     elif isinstance(data, ISBNValidationResult):
#         try:
#             handleISBNValidationResult(key, data)
#         except HandlerError,e:
#             print str(e)
#             pass
#         message.ack()            
#         #data.is_valid and "VALID" or "INVALID",
#         pass
#     elif isinstance(data, CountResult):
#         with api.env.adopt_user(username="system"):
#             createContentInContainer(systemMessages,'edeposit.content.isbncountresult', 
#                                      title="".join(["Výsledky dotazu na duplicitu ISBN: ",
#                                                     requestMessage.isbn,
#                                                     "(", str(data.num_of_records), ")"
#                                                 ]),
#                                      isbn = requestMessage.isbn,
#                                      num_of_records = data.num_of_records)
#         pass
#     elif isinstance(data, ExportResult):
#         print "export result from aleph"
#         with api.env.adopt_user(username="system"):
#             createContentInContainer(systemMessages,'edeposit.content.alephexportresult', 
#                                      title="".join(["Výsledky exportu do Aleph: ",
#                                                     requestMessage.isbn]),
#                                      isbn = requestMessage.isbn,
#                                  )
#         pass

#     elif "exception" in headers:
#         with api.env.adopt_user(username="system"):
#             if systemMessages:
#                 createContentInContainer(systemMessages,'edeposit.content.alephexception', 
#                                          title="".join([u"Chyba při volání služby Aleph: ",
#                                                         getattr(requestMessage,'isbn',""),
#                                                     ]),
#                                          message = "".join([ str(headers),
#                                                              str(data)
#                                                          ]),
#                                          isbn = getattr(requestMessage,'isbn',""),
#                                      )
#             else:
#                 print "exception without systemMessages folder, so I print it only", str(headers)
#             pass

#         print "There was an error in processing request ", headers["UUID"]
#         print headers["exception_name"] + ": " + headers["exception"]
#     else:
#         print "unknown message"
#         print message.body

#     message.ack()
#     pass
