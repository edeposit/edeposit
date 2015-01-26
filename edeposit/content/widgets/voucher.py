from zope.interface import implementer, implements, implementsOnly
from zope.component import adapter
from edeposit.content.originalfile import IVoucherFileField

from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager, NOVALUE
from z3c.form.widget import FieldWidget
from plone.formwidget.namedfile.widget import NamedFileWidget
from interfaces import IVoucherFileWidget

class VoucherFileWidget(NamedFileWidget):
    implements(IVoucherFileWidget)
    pass

@implementer(IFieldWidget)
@adapter(IVoucherFileField, IFormLayer)
def VoucherFileFieldWidget(field, request):
    return FieldWidget(field, VoucherFileWidget(request))
