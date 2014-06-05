# -*- coding: utf-8 -*-
from zope.component import queryUtility, getUtility
from zope.container.interfaces import (
    IObjectAddedEvent, 
    IObjectRemovedEvent,
    IContainerModifiedEvent
)
from logging import getLogger
logger = getLogger('edeposit.content.handlers')

from plone.dexterity.utils import createContentInContainer

from zope.interface import Interface
from plone import api
from edeposit.content import MessageFactory as _
from Acquisition import aq_inner, aq_parent
from edeposit.amqp.aleph import (
    ISBNQuery, 
    CountRequest, 
    ISBNValidationRequest,
    ExportRequest
)
from edeposit.amqp.serializers import (
    serialize,
    deserialize
)
from edeposit.amqp.aleph.datastructures.epublication import (
    EPublication,
    Author
)

from edeposit.amqp.aleph.datastructures.results import (
    ISBNValidationResult,
    CountResult,
    ExportResult,
)

from five import grok
from datetime import datetime

from collective.zamqp.interfaces import (
    IProducer, 
    IBrokerConnection,
    IConsumer
)
from collective.zamqp.interfaces import IMessageArrivedEvent
from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer
from collective.zamqp.connection import BlockingChannel
import json

class ISBNValidateRequestProducent(Producer):
    grok.name('amqp.isbn-validate-request')

    connection_id = "aleph"
    exchange = "validate"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    #routing_key = "plone.aleph.isbn.validate.request"
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
    #routing_key = "plone.aleph.isbn.count.request"
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
    headers = message.header_frame.headers
    key=headers.get('UUID',None)
    if not key:
        print "no UUID at headers"
        print message.body
        message.ack()
        return

    def getIfKeyExists(keyName,key):
        if key.get(keyName,None):
            return api.content.get(UID=key[keyName])
        return None

    keyContent = json.loads(key)
    systemMessages = getIfKeyExists('systemMessages_UID',keyContent)
    requestMessage = getIfKeyExists('request_UID',keyContent)
    if not systemMessages or not requestMessage:
        print "no system message or no request message exists in key"
        print message.body
        message.ack()
        return

    # Messages from Aleph has its own deserialization logic. 
    # So we will use it.
    data = deserialize(json.dumps(message.body),globals())
    print data
    if isinstance(data, ISBNValidationResult):
        with api.env.adopt_user(username="system"):
            createContentInContainer(systemMessages,'edeposit.content.isbnvalidationresult', 
                                     title="".join(["Výsledky kontroly ISBN: ",
                                                    requestMessage.isbn,
                                                    " (",
                                                    data.is_valid and "VALID" or "INVALID",
                                                    ")"]),
                                     isbn = requestMessage.isbn,
                                     is_valid = data.is_valid)
        pass
    elif isinstance(data, CountResult):
        with api.env.adopt_user(username="system"):
            createContentInContainer(systemMessages,'edeposit.content.isbncountresult', 
                                     title="".join(["Výsledky dotazu na duplicitu ISBN: ",
                                                    requestMessage.isbn,
                                                    "(", str(data.num_of_records), ")"
                                                ]),
                                     isbn = requestMessage.isbn,
                                     num_of_records = data.num_of_records)
        pass
    elif isinstance(data, ExportResult):
        print "export result from aleph"
        with api.env.adopt_user(username="system"):
            createContentInContainer(systemMessages,'edeposit.content.alephexportresult', 
                                     title="".join(["Výsledky exportu do Aleph: ",
                                                    requestMessage.isbn]),
                                     isbn = requestMessage.isbn,
                                 )
        pass

    elif "exception" in headers:
        with api.env.adopt_user(username="system"):
            createContentInContainer(systemMessages,'edeposit.content.alephexception', 
                                     title="".join([u"Chyba při volání služby Aleph: ",
                                                    requestMessage.isbn,
                                                ]),
                                     message = "".join([ str(headers),
                                                         str(data)
                                                     ]),
                                     isbn = requestMessage.isbn,
                                 )
            pass

        print "There was an error in processing request ", headers["UUID"]
        print headers["exception_name"] + ": " + headers["exception"]
    else:
        print "unknown message"
        print message.body

    message.ack()
    pass

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
    context.invokeFactory('edeposit.content.messagesfolder','system-messages',
                          title=u"Systémové zprávy")

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
    #routing_key = "plone.aleph.isbn.count.request"
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
        zpracovatelZaznamu = epublication.zpracovatel_zaznamu or "",
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

def addedAlephExportResult(context, event):
    logger.debug('added aleph export result')
    wft = api.portal.get_tool('portal_workflow')
    systemMessages = aq_parent(aq_inner(context))
    epublication = aq_parent(aq_inner(systemMessages))
    print "added aleph export result"
    # request = AlephExportRequest(context.isbn)
    # producer = getUtility(IProducer, name="amqp.aleph-export-result")
    wft.doActionFor(epublication, 'exportToAlephOK')
    return
