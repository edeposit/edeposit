# -*- coding: utf-8 -*-

from plone import api
from zope.interface import Interface, Attribute, implements, classImplements
from zope.component import getUtility, getAdapter, getMultiAdapter
from Acquisition import aq_parent, aq_inner
from plone.namedfile.file import NamedBlobFile
from base64 import b64encode, b64decode
from plone.dexterity.utils import createContentInContainer, addContentToContainer, createContent
import transaction
from itertools import takewhile

from .next_step import INextStep

from edeposit.amqp.aleph import (
    ISBNQuery, 
    GenericQuery, 
    CountRequest, 
    SearchRequest, 
    DocumentQuery,
    ISBNValidationRequest,
    ExportRequest
)

from edeposit.amqp.serializers import (
    serialize,
    deserialize
)
from edeposit.amqp.aleph.datastructures.epublication import (
    EPublication,
    Author
)

from edeposit.amqp.aleph.datastructures.semanticinfo import (
    SemanticInfo
)

from edeposit.amqp.aleph.datastructures.alephrecord import (
    AlephRecord
)

from edeposit.amqp.aleph.datastructures.results import (
    ISBNValidationResult,
    CountResult,
    SearchResult,
    ExportResult,
)

from edeposit.amqp.antivirus.structures import (
    ScanResult,
    ScanFile
)

from edeposit.amqp.calibre.structures import (
    ConversionRequest,
    ConversionResponse
)

from collective.zamqp.producer import Producer
from collective.zamqp.consumer import Consumer
from collective.zamqp.connection import BlockingChannel
from collective.zamqp.interfaces import (
    IProducer, 
    IConsumer
)

from five import grok
import json
import base64
from zope.component import getUtility

class AntivirusCheckRequestProducent(Producer):
    grok.name('amqp.antivirus-request')

    connection_id = "antivirus"
    exchange = "antivirus"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass

class ISBNValidationRequestProducent(Producer):
    grok.name('amqp.isbn-validation')

    connection_id = "aleph"
    exchange = "validate"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass

class ISBNSearchRequestProducent(Producer):
    grok.name('amqp.isbn-search-request')

    connection_id = "aleph"
    exchange = "search"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass

class CalibreConvertProducent(Producer):
    grok.name('amqp.calibre-convert-request')

    connection_id = "calibre"
    exchange = "convert"
    serializer = "text/plain"
    exchange_type = "topic"
    exchange_durable = True
    auto_delete = False
    durable = True
    routing_key = "request"
    pass


class IScanResult(Interface):
    result = Attribute("")
    filename = Attribute("")
classImplements(ScanResult, IScanResult)

class IISBNValidationResult(Interface):
    is_valid = Attribute("")
classImplements(ISBNValidationResult, IISBNValidationResult)

class ICountResult(Interface):
    num_of_records = Attribute("")
classImplements(CountResult, ICountResult)

class IAlephExportResult(Interface):
    ISBN = Attribute("")
classImplements(ExportResult, IAlephExportResult)

class IAlephSearchResult(Interface):
    records = Attribute("List os AlephRecords")
classImplements(SearchResult, IAlephSearchResult)

class ICalibreConversionResult(Interface):
    type = Attribute("")
    b64_data = Attribute("")
    protocol = Attribute("")
classImplements(ConversionResponse, ICalibreConversionResult)

class IAMQPSender(Interface):
    """
    """
    
    def send():
        pass
    

class IAMQPHandler(Interface):
    """
    """

    def handle():
        return None


def make_headers(context, session_data):
    return {
        'UUID': json.dumps({'context_UID': str(context.UID()),
                            'session_data': session_data
                        })
    }

def parse_headers(headers):
    uuid = headers['UUID']
    data = json.loads(uuid)
    uid = data.get('context_UID',None)
    context = uid and api.content.get(UID=uid)
    return (context, data['session_data'])

from collections import namedtuple

class OriginalFileThumbnailRequestSender(namedtuple('ThumbnailGeneratingRequest',['context'])):
    implements(IAMQPSender)
    def send(self):
        print "-> Thumbnail Generating Request"
        originalfile = self.context
        fileName = originalfile.file.filename
        inputFormat = "epub"
        request = ConversionRequest(inputFormat, "pdf", base64.b64encode(originalfile.file.data))
        producer = getUtility(IProducer, name="amqp.calibre-convert-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'filename': fileName,
                          'msg': msg
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request), content_type = 'application/json', headers = headers )
    pass

class OriginalFileAntivirusRequestSender(namedtuple('AntivirusRequest',['context'])):
    implements(IAMQPSender)
    def send(self):
        print "-> Antivirus Request"
        originalfile = self.context
        fileName = originalfile.file.filename
        request = ScanFile(fileName, base64.b64encode(originalfile.file.data))
        producer = getUtility(IProducer, name="amqp.antivirus-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request), content_type = 'application/json', headers = headers )
    pass

class OriginalFileISNBValidateRequestSender(namedtuple('ISBNValidateRequest',['context'])):
    """ context will be original file """
    implements(IAMQPSender)
    def send(self):
        print "-> ISBN Validation Request"
        request = ISBNValidationRequest(self.context.isbn)
        producer = getUtility(IProducer, name="amqp.isbn-validate-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request),  content_type = 'application/json', headers = headers)
        pass

class OriginalFileISNBDuplicityCheckRequestSender(namedtuple('ISBNDuplicityCheckRequest',['context'])):
    """ context will be original file """
    implements(IAMQPSender)
    def send(self):
        print "-> ISBN Duplicity Check Request"
        request = CountRequest(ISBNQuery(self.context.isbn))
        producer = getUtility(IProducer, name="amqp.isbn-count-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request),  content_type = 'application/json', headers = headers)
        pass


class OriginalFileExportToAlephRequestSender(namedtuple('ExportToAlephRequest',['context'])):
    """ context will be original file """
    implements(IAMQPSender)
    def send(self):
        print "-> ISBN Export To Aleph Request"
        originalFile = self.context
        epublication = aq_parent(aq_inner(originalFile))
        authors = map(lambda aa: Author(lastName = aa.fullname, firstName="", title = ""), epublication.authors.results())
        epublicationRecord =  EPublication (
            ISBN = originalFile.isbn or "",
            nazev = epublication.title or "",
            podnazev = epublication.podnazev or "",
            vazba = "online",
            cena = str(epublication.cena or ""),
            castDil = epublication.cast or "",
            nazevCasti = epublication.nazev_casti or "",
            nakladatelVydavatel = epublication.nakladatel_vydavatel or "",
            datumVydani = str(epublication.rok_vydani),
            poradiVydani = epublication.poradi_vydani or "",
            zpracovatelZaznamu = epublication.zpracovatel_zaznamu or "",
            format = originalFile.format or "",
            url = originalFile.url or "",
            mistoVydani = epublication.misto_vydani,
            ISBNSouboruPublikaci = epublication.isbn_souboru_publikaci or "",
            autori = map(lambda author: author.lastName, filter(lambda author: author.lastName, authors)),
            originaly = [],
            internal_url = originalFile.absolute_url() or "",
        )
        request = ExportRequest(epublication=epublicationRecord)
        producer = getUtility(IProducer, name="amqp.aleph-export-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request),  content_type = 'application/json', headers = headers)
        pass

class OriginalFileSysNumberSearchRequestSender(namedtuple('SysNumberSearchRequest',['context'])):
    """ context will be original file """
    implements(IAMQPSender)
    def send(self):
        print "-> SysNumber search Request"
        request = SearchRequest(ISBNQuery(self.context.isbn, 'cze-dep'))
        producer = getUtility(IProducer, name="amqp.isbn-search-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg,
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request),  content_type = 'application/json', headers = headers)
        pass


class OriginalFileRenewAlephRecordsRequestSender(namedtuple('RenewAlephRecordsRequest',['context'])):
    """ context will be original file """
    implements(IAMQPSender)
    def send(self):
        print "-> Renew Aleph Records Request"
        request = SearchRequest(ISBNQuery(self.context.isbn,'cze-dep'))
        producer = getUtility(IProducer, name="amqp.isbn-search-request")
        msg = ""
        session_data =  { 'isbn': str(self.context.isbn),
                          'msg': msg,
        }
        headers = make_headers(self.context, session_data)
        producer.publish(serialize(request),  content_type = 'application/json', headers = headers)
        pass


class OriginalFileAntivirusResultHandler(namedtuple('AntivirusResult',['context', 'result'])):
    implements(IAMQPHandler)
    def handle(self):
        print "<- Antivirus Result"
        wft = api.portal.get_tool('portal_workflow')
        result = self.result
        context = self.context
        epublication=aq_parent(aq_inner(context))
        with api.env.adopt_user(username="system"):
            if result.result: # some virus found
                comment =u"v souboru %s je virus: %s" % (context.file.filename, str(result.result))
                wft.doActionFor(epublication,'notifySystemAction', comment=comment)
                wft.doActionFor(context, 'antivirusError', comment=comment)
            else:
                comment=u"soubor %s prošel antivirovou kontrolou" % (context.file.filename,)
                wft.doActionFor(epublication,'notifySystemAction', comment=comment)
                transition =  context.needsThumbnailGeneration() and 'antivirusOKThumbnail' \
                              or (context.isbn and 'antivirusOKAleph' or 'antivirusOKISBNGeneration')
                print "transition: %s" % (transition,)
                wft.doActionFor(context, transition)
            pass
        pass

class OriginalFileThumbnailGeneratingResultHandler(namedtuple('ThumbnailGeneratingResult',
                                                              ['context','result'])):
    """ 
    context: originalfile
    result:  ThumbnailGeneratingResult
    """
    def handle(self):
        print "<- Calibre Thumbnail Generating Result"
        wft = api.portal.get_tool('portal_workflow')
        epublication=aq_parent(aq_inner(self.context))
        with api.env.adopt_user(username="system"):
            comment = u"hurá, máme náhled! %s" % (self.context.file.filename, )
            bfile = NamedBlobFile(data=b64decode(self.result.b64_data),  filename=u"thumbnail.pdf")
            previewFileData = { 'file': bfile }
            previewFile = createContentInContainer(self.context, 
                                                   'edeposit.content.previewfile',
                                                   **previewFileData)
            transaction.savepoint(optimistic=True)
            wft.doActionFor(epublication,'notifySystemAction', comment=comment)
            wft.doActionFor(self.context, 'thumbnailOK')
        pass


class OriginalFileISBNValidateResultHandler(namedtuple('ISBNValidateResult',['context', 'result'])):
    """ 
    context: originalfile
    result:  ISBNValidationResult
    """
    def handle(self):
        print "<- ISBN Validation result"
        wft = api.portal.get_tool('portal_workflow')
        epublication=aq_parent(aq_inner(self.context))
        with api.env.adopt_user(username="system"):
            comment = u"výsledek kontroly ISBN(%s): %s" % (self.context.isbn, 
                                                           self.result.is_valid and "VALID" or "INVALID")
            wft.doActionFor(epublication,'notifySystemAction', comment=comment)
            wft.doActionFor(self.context, self.result.is_valid and 'ISBNIsValid' or 'ISBNIsNotValid')
        pass

class OriginalFileCountResultHandler(namedtuple('ISBNCountResult',['context', 'result'])):
    """ 
    context: originalfile
    result:  CountResult
    """
    def handle(self):
        print "<- Aleph Count result"
        wft = api.portal.get_tool('portal_workflow')
        epublication=aq_parent(aq_inner(self.context))
        is_duplicit = bool(int(self.result.num_of_records))
        with api.env.adopt_user(username="system"):
            comment = u"výsledek kontroly duplicity ISBN(%s): %s" % (self.context.isbn, 
                                                                     self.result.num_of_records)
            wft.doActionFor(epublication,'notifySystemAction', comment=comment)
            wft.doActionFor(self.context, is_duplicit and 'ISBNIsDuplicit' or 'ISBNIsUnique')
        pass


class OriginalFileAlephExportResultHandler(namedtuple('AlephResultResult',['context', 'result'])):
    """ 
    context: originalfile
    result:  CountResult
    """
    def handle(self):
        print "<- Aleph Export result"
        wft = api.portal.get_tool('portal_workflow')
        epublication=aq_parent(aq_inner(self.context))
        with api.env.adopt_user(username="system"):
            comment = u"export do Aleph proběhl úspěšně (%s)" % (self.result.ISBN,)
            wft.doActionFor(epublication,'notifySystemAction', comment=comment)
            wft.doActionFor(self.context, 'exportToAlephOK')
        pass

class OriginalFileAlephSearchResultHandler(namedtuple('AlephSearchtResult',['context', 'result'])):
    """ 
    context: originalfile
    result:  SearchResult
    """
    def handle(self):
        print "<- Aleph Search result"
        with api.env.adopt_user(username="system"):
            for record in self.result.records:
                epublication = record.epublication
                dataForFactory = {
                    'title': "".join([u"Záznam v Alephu: ",
                                      str(epublication.nazev), 
                                      '(', 
                                      str(record.docNumber),
                                      ')']),
                    'nazev':  str(epublication.nazev),
                    'isbn': epublication.ISBN[0],
                    'podnazev': epublication.podnazev,
                    'cast': epublication.castDil,
                    'nazev_casti': epublication.nazevCasti,
                    'rok_vydani': epublication.datumVydani,
                    'aleph_sys_number': record.docNumber,
                    'aleph_library': record.library,
                    'hasAcquisitionFields': record.semantic_info.hasAcquisitionFields,
                    'hasISBNAgencyFields': record.semantic_info.hasISBNAgencyFields,
                    }
                self.context.updateOrAddAlephRecord(dataForFactory)
                pass

            takewhile(lambda x: INextStep(self.context).doActionFor(), range(5))
        pass


class OriginalFileExceptionHandler(namedtuple('ExceptionHandler',['context', 'result'])):
    """ 
    context: originalfile
    result:  AMQPError
    """
    def handle(self):
        print "<- Aleph Exception"
        wft = api.portal.get_tool('portal_workflow')
        print self.result
        with api.env.adopt_user(username="system"):
            wft.doActionFor(self.context,'amqpError', comment=str(self.result.payload))
            wft.doActionFor(aq_parent(aq_inner(self.context)),'notifySystemAction', comment=str(self.result.payload))
        pass

