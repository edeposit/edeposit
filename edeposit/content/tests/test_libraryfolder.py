import unittest2 as unittest
import doctest

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

class TestLibraryFolder(unittest.TestCase):
    layer = EDEPOSIT_CONTENT_INTEGRATION_TESTING

    def test_doctest(self):
        #doctest.testfile("../LibraryFolder.txt")
        pass

    def test_creation(self):
        portal = self.layer['portal']
        # Ensure that we can create the various content types without error
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('edeposit.content.libraryfolder', 'elf1', title=u"E-Deposit Library Folder")
        setRoles(portal, TEST_USER_ID, ('Member',))

    def test_creation_library(self):
        portal = self.layer['portal']
        # Ensure that we can create the various content types without error
        setRoles(portal, TEST_USER_ID, ('Manager',))
        portal.invokeFactory('edeposit.content.libraryfolder', 'edlf1', title=u"E-Deposit Library Folder")
        setRoles(portal, TEST_USER_ID, ('Member',))
        portal['edlf1'].invokeFactory('edeposit.content.libraryfolder', 'edlf2', title=u"E-Deposit Library Folder")
        portal['edlf1'].invokeFactory('edeposit.content.library', 'edll1', title=u"E-Deposit Library")
