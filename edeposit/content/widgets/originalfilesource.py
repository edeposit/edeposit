from zope.interface import implementer, implements, implementsOnly
from zope.component import adapter
from edeposit.content.originalfile import IOriginalFileSourceField
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager, NOVALUE
from z3c.form.widget import FieldWidget
from plone.formwidget.namedfile.widget import NamedFileWidget
from interfaces import IOriginalFileSourceWidget
from plone.z3cform.layout import FormWrapper
from plone import api

class OriginalFileSourceWidget(NamedFileWidget):
    implements(IOriginalFileSourceWidget)

    @property
    def can_change(self):
        mtool = api.portal.get_tool('portal_membership')
        return mtool.checkPermission('Modify portal content', self.context)
    pass

@implementer(IFieldWidget)
@adapter(IOriginalFileSourceField, IFormLayer)
def OriginalFileSourceFieldWidget(field, request):
    return FieldWidget(field, OriginalFileSourceWidget(request))
