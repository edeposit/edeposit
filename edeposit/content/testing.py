from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from zope.configuration import xmlconfig

class EDepositContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import edeposit.content
        xmlconfig.file('configure.zcml', edeposit.content, context=configurationContext)
    
    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edeposit.content:default')

EDEPOSIT_CONTENT_FIXTURE = EDepositContent()
EDEPOSIT_CONTENT_INTEGRATION_TESTING = IntegrationTesting(bases=(EDEPOSIT_CONTENT_FIXTURE,), name="EDepositContent:Integration")
