# -*- coding: utf-8 -*-

from plone import api
from zope.interface import Interface, Attribute, implements, classImplements
from zope.component import getUtility, getAdapter, getMultiAdapter
from Acquisition import aq_parent, aq_inner
from plone.namedfile.file import NamedBlobFile
from base64 import b64encode, b64decode
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import transaction
from functools import wraps
from collections import namedtuple

class INextStep(Interface):
    """
    There is one step you can doActionFor automaticaly.
    """
    
    def doActionFor(self,*args,**kwargs):
        return False


class OriginalFileNextStep(namedtuple("OriginalFileNextStep",['context',])):
    def doActionFor(self,*args,**kwargs):
        self.wft = api.portal.get_tool('portal_workflow')
        review_state = api.content.get_state(self.context)
        fname="nextstep_for_%s" % (str(review_state),)
        print "... %s" % (fname,)
        fun = getattr(self,fname,None)
        wasNextStep = fun and fun(*args,**kwargs)
        return wasNextStep

    def nextstep_for_acquisition(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasAcquisitionFields:
            self.wft.doActionFor(self.context,'submitAcquisition')
            self.wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment="submit Acquisition")
            return True
        return False

    def nextstep_for_state_ISBNGeneration(self, *args, **kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasISBNAgencyFields:
            self.wft.doActionFor(self.context,'submitISBNGeneration')
            self.wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment="ISBN was assigned")
            return True
        return False

    def nextstep_for_waitingForAleph(self,*args,**kwargs):
        alephRecords = self.context.listFolderContents(contentFilter={'portal_type':'edeposit.content.alephrecord'})
        if not alephRecords:
            comment = u"v Alephu není žádný záznam.  ISBN: %s" % (self.context.isbn, )
            self.wft.doActionFor(self.context,'noAlephRecordLoaded')
            self.wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment=comment)
            return False

        comment = u"výsledek dotazu do Alephu ISBN(%s): zaznamu: %s" % (self.context.isbn, 
                                                                        str(len(alephRecords)))
        
        self.wft.doActionFor(self.context, 'alephRecordsLoaded')
        self.wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment=comment)
        return True
        
    def nextstep_for_descriptiveCataloguing(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasDescriptiveCataloguingFields:
            self.wft.doActionFor(self.context,'submitDescriptiveCataloguing')
            return True
        return False

    def nextstep_for_descriptiveCataloguingReview(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasDescriptiveCataloguingReviewFields:
            self.wft.doActionFor(self.context,'submitDescriptiveCataloguingReview')
            return True
        return False

    def nextstep_for_subjectCataloguing(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasSubjectCataloguingFields:
            self.wft.doActionFor(self.context,'submitSubjectCataloguing')
            return True
        return False

    def nextstep_for_subjectCataloguingReview(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasSubjectCataloguingReviewFields:
            self.wft.doActionFor(self.context,'submitSubjectCataloguingReview')
            return True
        return False

    def nextstep_for_ISBNSubjectValidation(self,*args,**kwargs):
        aleph_record = self.context.related_aleph_record and getattr(self.context.related_aleph_record,'to_object',None)
        if aleph_record and aleph_record.hasISBNAgencyFields:
            self.wft.doActionFor(self.context,'submitISBNSubjectValidation')
            return True
        return False
