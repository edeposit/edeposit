# -*- coding: utf-8 -*-

from plone import api
from zope.interface import Interface, Attribute, implements, classImplements
from zope.component import getUtility, getAdapter, getMultiAdapter
from Acquisition import aq_parent, aq_inner
from plone.namedfile.file import NamedBlobFile
from base64 import b64encode, b64decode
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import transaction

from collections import namedtuple

class INextStep(Interface):
    """
    There is one step you can doActionFor automaticaly.
    """
    
    def doActionFor(self,*args,**kwargs):
        return False


class OriginalFileNextStep(namedtuple("OriginalFileNextStep",['context',])):
    def doActionFor(self,*args,**kwargs):
        print "original file automatic next step"
        review_state = api.content.get_state(self.context)
        fname="nextstep_for_%s" % (str(review_state),)
        fun = getattr(self,fname,None)
        wasNextStep = fun and fun(*args,**kwargs)
        return False

    def nextstep_for_waitingForAcquisition(self,*args,**kwargs):
        return False

    def nextstep_for_waitingForAleph(self,*args,**kwargs):
        wft = api.portal.get_tool('portal_workflow')
        alephRecords = self.context.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})
        if not alephRecords:
            comment = u"v Alephu není žádný záznam.  ISBN: %s" % (self.context.isbn, )
            wft.doActionFor(self.context,'noAlephRecordLoaded')
            wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment=comment)
            return False

        comment = u"výsledek dotazu do Alephu ISBN(%s): zaznamu: %s" % (self.context.isbn, 
                                                                        str(len(alephRecords)))
        
        wft.doActionFor(self.context, 'alephRecordsLoaded')
        wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment=comment)
        return True
