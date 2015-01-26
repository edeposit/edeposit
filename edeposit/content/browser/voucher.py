# -*- coding: utf-8 -*-
from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.deprecation.deprecation import deprecate
from zope.i18n import translate
from zope.interface import implements, alsoProvides, Interface
from zope.viewlet.interfaces import IViewlet

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from plone.directives import form
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IContentViews, IBelowContent, IAboveContentBody, IBelowContentBody
from plone.app.layout.viewlets import ViewletBase

from plone import api
from edeposit.user.producent import IProducent

from plone.app.contentmenu import menu
from plone.app.contentmenu.interfaces import IWorkflowSubMenuItem
from plone.z3cform.layout import FormWrapper

from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
import json

class VoucherDownload(BrowserView):
    def __call__(self):
        file_ = self.context.voucher

        if not file_:
            raise NotFound(self, 'ohlasovaci-listek.pdf', self.request)

        set_headers(file_, self.request.response, filename="ohlasovaci-listek.pdf")
        return stream_data(file_)

class GenerateVoucher(BrowserView):
    def __call__(self):
        with api.env.adopt_user(username="system"):
            wft = api.portal.get_tool('portal_workflow')
            wft.doActionFor(self.context,'generateVoucher')
            
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(dict(done = True))

class HasVoucher(BrowserView):
    def __call__(self):
        file_ = self.context.voucher
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(dict(has_voucher = bool(file_)))
