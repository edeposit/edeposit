# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute, implements, classImplements
from zope.component import getUtility, getAdapter, getMultiAdapter, adapts, provideAdapter
from zope import schema
from collections import namedtuple
import json
from edeposit.amqp.serializers import serialize
from collective.zamqp.interfaces import (
    IProducer, 
)

"""
(add-hook 'after-save-hook 'restart-pdb-instance nil t)
"""

class IPloneTask(Interface):
    pass

class IJSONEncoder(Interface):
    def encode():
        pass

class JSONEncoderForIPloneTask(namedtuple('JSOEncoder',['context'])):
    adapts(IPloneTask)
    implements(IJSONEncoder)

    def encode(self):
        return serialize(self.context)
        
provideAdapter(JSONEncoderForIPloneTask)

class IPloneTaskSender(Interface):
    """ send plone task """
    def send():
        pass

class PloneTaskSender(namedtuple('PloneTaskSender',['context'])):    
    adapts(IPloneTask)
    implements(IPloneTaskSender)

    def send(self):
        payload = IJSONEncoder(self.context).encode()
        producer = getUtility(IProducer, name="amqp.plone-task-request")
        producer.publish(payload, content_type="application/json", headers={})
        pass

provideAdapter(PloneTaskSender)

class ISendEmailWithWorklistToGroup(IPloneTask):
    worklist = schema.ASCIILine()
    recipientsGroup = schema.ASCIILine()
    additionalEmails = schema.List (
        value_type = schema.ASCIILine()
    )
    subject = schema.TextLine()

class SendEmailWithWorklistToGroup(namedtuple('SendEmailWithWorklistToGroup',
                                              ['worklist','recipientsGroup','additionalEmails','subject'])):
    implements(ISendEmailWithWorklistToGroup)
    pass

class ILoadSysNumbersFromAleph(IPloneTask):
    pass

class LoadSysNumbersFromAleph(namedtuple('LoadSysNumbersFromAleph',[])):
    implements(ILoadSysNumbersFromAleph)
    pass

class IRenewAlephRecords(IPloneTask):
    pass

class RenewAlephRecords(namedtuple('RenewAlephRecords',[])):
    implements(IRenewAlephRecords)
    pass

class IDoActionFor(IPloneTask):
    uid = schema.ASCIILine()
    transition = schema.ASCIILine()
    pass

class DoActionFor(namedtuple('DoActionFor',['uid','transition'])):
    implements(IDoActionFor)
    pass

class ISendEmailWithUserWorklist(IPloneTask):
    worklist = schema.ASCIILine()
    groupname = schema.ASCIILine()
    additionalEmails = schema.List(
        value_type = schema.ASCIILine()
    )

class SendEmailWithUserWorklist(namedtuple('SendEmailWithUserWorklist',
                                           ['worklist','groupname','additionalEmails'])):
    implements(ISendEmailWithUserWorklist)
    pass

class ISendEmailWithUserWorklist(IPloneTask):
    title = schema.TextLine()
    groupname = schema.ASCIILine()
    additionalEmails = schema.List(
        value_type = schema.ASCIILine()
    )

if __name__ == '__main__':
    import unittest

    # class PloneTaskProducer(Producer):
    #     """
    #     """
    #     connection_id = "plone"
    #     exchange = "task"
    #     exchange_type = "topic"
    #     echange_durable = True
    #     auto_delete = False
    #     durable = True
    #     routing_key = "execute"
        
    #     def __init__(self, ):
    #         """
    #         """
            
    class TestCase(unittest.TestCase):
        
        def test_01(self):
            task = SendEmailWithWorklistToGroup (
                worklist = "worklist-originalfiles-waiting-for-isn-agency",
                recipientsGroup = "ISBN Agency Members",
                additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                subject = u"Nějaký email"
            )
            assert(ISendEmailWithWorklistToGroup.providedBy(task))
            result = IJSONEncoder(task).encode()
            assert (frozenset(json.loads(result).keys()) == frozenset([u'recipientsGroup', u'worklist', u'additionalEmails', 'subject', u'__nt_name']))
            pass

        def test_02(self):
            task = SendEmailWithWorklistToGroup (
                worklist = "worklist-originalfiles-waiting-for-isn-agency",
                recipientsGroup = "ISBN Agency Members",
                additionalEmails = ['stavel.jan@gmail.com','alena.zalejska@pragodata.cz'],
                subject = u"Nějaký email"
            )
            #send = IPublishPloneTask(task).publish()
            
    unittest.main()
    
