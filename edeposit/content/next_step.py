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
    def doActionFor(self,*args,**kwards):
        print "original file automatic next step"
        wft = api.portal.get_tool('portal_workflow')
        review_state = wft.getStatusOf("plone_workflow", object).get('review_state',None)
        if review_state:
            fname="nextstep_for_state_%s" % (review_state,)
            if getattr(self,fname,None):
                wasNextStep = fname(*args,**kwargs)
                return wasNextStep
        return False


    def nextstep_for_state_waitingForAcquisition(self,*args,**kwargs):
        return False

    def nextstep_for_state_ISBNGeneratinng(self, *args, **kwargs):
        return False
