# coding: utf-8 -*-

from zope.interface import implementer, alsoProvides, implements
from zope.component import adapter, adapts

from edeposit.content.behaviors import (
    IFormat, 
    ICalibreFormat
)

from edeposit.content.originalfile import IOriginalFile

@implementer(IFormat)
@adapter(IOriginalFile)
class Format(object):
    """Store format in the Dublin Core metadata Subject field. This makes
    tags easy to search for.
    """

    def __init__(self, context):
        self.context = context

    @property
    def format(self):
        if self.context.file:
            fileFormat = magic.from_buffer(self.context.file.data)
            print "identified: %s for file: %s" % (fileFormat, str(self.context))
            txt = fileFormat.lower()
            shortFormat = (('mobipocket' in txt) and 'Mobi') or \
                          (('epub' in txt) and 'EPub') or \
                          (('pdf' in txt) and 'PDF') or fileFormat
            
            print "format format is: ", shortFormat
            return shortFormat

        return 'text/html'

class CalibreFormat(object):
    implements(ICalibreFormat)
    adapts(IOriginalFile)

    def __init__(self, context):
        self.context = context

    @property
    def format(self):
        format = IFormat(self.context).format
        return format.lower()
