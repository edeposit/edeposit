import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from edeposit.content.testing import EDEPOSIT_CONTENT_INTEGRATION_TESTING

from zope.interface import Invalid
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.event import notify

from zope.schema.interfaces import IVocabularyFactory

from zope.intid.interfaces import IIntIds
from z3c.relationfield import RelationValue

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.event import ObjectInitializedEvent

class TestContent(unittest.TestCase):

    layer = EDEPOSIT_CONTENT_INTEGRATION_TESTING

    def test_hierarchy(self):
        portal = self.layer['portal']
        
        # Ensure that we can create the various content types without error
        
        setRoles(portal, TEST_USER_ID, ('Manager',))
        
        portal.invokeFactory('edeposit.EBookFolder', 'ebf1', title=u"E-Deposit ebook folder")
        
        setRoles(portal, TEST_USER_ID, ('Member',))
        
        portal['ebf1'].invokeFactory('edeposit.EBook', 'eb1', title=u"EBook")
        # portal['cf1']['c1'].invokeFactory('optilux.Promotion', 'p1', title=u"Promotion")
        
        # portal['ff1'].invokeFactory('optilux.Film', 'f1', title=u"Film")
    
