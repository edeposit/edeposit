# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent,\
    IContainerModifiedEvent
from zope.interface import Interface
from plone import api
from edeposit.content import MessageFactory as _

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
            
    
def addedISBNCheckRequest(context, event):
    #wft = api.portal.get_tool('portal_workflow')
    #wft.doActionFor(epublication,"notifySystemAction", comment=title)
    print "added isbn check request"
    return

def addedISBNCountRequest(context, event):
    #wft = api.portal.get_tool('portal_workflow')
    #wft.doActionFor(epublication,"notifySystemAction", comment=title)
    print "added isbn count request"
    return

def addedISBNCheckResponse(context, event):
    print "added isbn check response"
    return

def addedISBNCountResponse(context, event):
    print "added isbn count response"
    return
