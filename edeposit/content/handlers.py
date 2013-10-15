# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.container.interfaces import IObjectAddedEvent, IObjectRemovedEvent,\
    IContainerModifiedEvent
from zope.interface import Interface

from edeposit.user import MessageFactory as _

def added(context,event):
    """When an object is added, create collection for simple list of authors
    """
    context.invokeFactory('Collection','authors',
                          title=_(u"Review of authors"),
                          query=[{'i': 'portal_type',
                                  'o': 'plone.app.querystring.operation.selection.is',
                                  'v': 'edeposit.content.author'},
                                 {'i': 'path', 
                                  'o': 'plone.app.querystring.operation.string.relativePath', 
                                  'v': '../'}
                                 ]
                          )

    context.invokeFactory('Collection','isbns', 
                          title=_(u"Review of ISBNs"),
                          query=[{'i': 'portal_type', 
                                  'o': 'plone.app.querystring.operation.selection.is', 
                                  'v': 'edeposit.content.isbn'
                                  },
                                 {'i': 'path', 
                                  'o': 'plone.app.querystring.operation.string.relativePath', 
                                  'v': '../'}
                                 ],
                          )
    
