from cgi import escape
from datetime import date
from urllib import unquote

from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements, alsoProvides, Interface
from zope.viewlet.interfaces import IViewlet

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

from five import grok
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IContentViews, IBelowContent
from plone.app.layout.viewlets import ViewletBase

from plone import api
from originalfile import IOriginalFile
from epublication import IePublication

from plone.app.contentmenu import menu
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem

class ContentState(grok.Viewlet):
    grok.name('edeposit.contentstate')
    grok.require('zope2.View')
    grok.viewletmanager(IContentViews)
    grok.view(IViewView)
    grok.context(IOriginalFile)

    def update(self):
        super(ContentState,self).update()
        context = aq_inner(self.context)
        plone_utils = api.portal.get_tool('plone_utils')

        wft = api.portal.get_tool('portal_workflow')
        state = api.content.get_state(obj=context)
        stateTitle = wft.getTitleForStateOnType(state,context.portal_type)

        self.wf_state = dict( state = state, 
                              title = stateTitle,
                              stateClass = 'contentstate-'+plone_utils.normalizeString(state),
                              href = context.absolute_url() + "/content_status_history",
                              )
        wf_tool = getToolByName(self.context, 'portal_workflow')
        infos = filter(lambda info: info.get('available',None) and info.get('category',None) == 'workflow', wf_tool.listActionInfos(object=self.context))
        self.transitions = infos
        return


class ContentStateForEPublication(ContentState):
    grok.name('edeposit.contentstateforepublication')
    grok.require('zope2.View')
    grok.viewletmanager(IContentViews)
    #grok.view(IViewView)
    grok.context(IePublication)
    grok.template('viewlets_templates/contentstate.pt')

class ContentHistory(grok.Viewlet):
    grok.name('edeposit.contenthistory')
    grok.require('zope2.View')
    grok.viewletmanager(IBelowContent)
    #grok.view(IViewView)
    grok.context(IOriginalFile)


