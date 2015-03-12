from .originalfile import IOriginalFile
from .changes import IChanges, ObjSetterApply
from zope.interface import implements
from zope.component import adapts
from Acquisition import aq_parent, aq_inner

class OriginalFileChanges(object):
    implements(IChanges)
    adapts(IOriginalFile)

    def __init__(self, context):
        self.context = context
        self.epublication = aq_parent(aq_inner(self.context))
    
    def changesFromAlephRecord(self,record):
        changes = []

        if record.isbn != self.context.isbn:
            changes.append(ObjSetterApply(self.context, 'isbn', record.isbn))

        if record.nazev != self.epublication.title:
            changes.append(ObjSetterApply(self.epublication, 'title', record.nazev))

        if record.podnazev != self.epublication.podnazev:
            changes.append(ObjSetterApply(self.epublication, 'podnazev', record.podnazev))
            
        if record.nazev_casti != self.epublication.nazev_casti:
            changes.append(ObjSetterApply(self.epublication, 'nazev_casti', record.nazev_casti))

        if record.rok_vydani != self.epublication.rok_vydani:
            changes.append(ObjSetterApply(self.epublication, 'rok_vydani', record.rok_vydani))

        return changes

    def getChanges(self):
        of = self.context

        related_aleph_record = of.related_aleph_record and getattr(of.related_aleph_record,'to_object',None)
        summary_aleph_record = of.summary_aleph_record and getattr(of.summary_aleph_record,'to_object',None)
        
        isClosed = related_aleph_record and related_aleph_record.isClosed
        hasRelatedAlephRecord = bool(related_aleph_record)
        hasSummary = bool(summary_aleph_record)

        if hasRelatedAlephRecord and not isClosed:
            return self.changesFromAlephRecord(related_aleph_record)
            
        if isClosed and hasSummary:
            return self.changesFromAlephRecord(summary_aleph_record)

        return []
