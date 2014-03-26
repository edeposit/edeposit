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
    serialize, 
    deserialize
)
from edeposit.amqp.aleph.datastructures.results import (
    ISBNValidationResult,
    CountResult
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
    key=message.header_frame.headers.get('UUID',None)
    if not key:
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
        message.ack()
        return

    # Messages from Aleph has its own deserialization logic. 
    # So we will use it.
    data = deserialize(json.dumps(message.body))
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

