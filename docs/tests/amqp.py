#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# library for Robot Framework to work with RabbitMQ
#

import pika
import json
from pyrabbit.api import Client
        
class RabbitMQ(object):
    def __init__(self):
        def createConnection(vhost):
            return pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost',
                virtual_host=vhost,
            )
        )
        self.connections = dict([(vhost, createConnection(vhost)) for vhost in ('aleph','antivirus','calibre','ftp')])
        self.channels = dict([(vhost, connection.channel()) for vhost,connection in self.connections.items()])
        self.client = Client('localhost:15672', 'guest', 'guest')

    def declare_queue(self, vhost, queue_name, durable=False):
        self.channels[vhost].queue_declare(queue=queue_name, durable=durable)        

    def delete_queue(self, vhost, queue_name):
        self.channels[vhost].queue_delete(queue=queue_name)
        
    def declare_queue_binding(self, vhost, exchange_name,  queue_name,  routing_key):
        self.channels[vhost].queue_bind( 
            exchange = str(exchange_name),
            queue = str(queue_name),
            routing_key = str(routing_key)
        )
        
    def get_message_from_queue(self, vhost, queue_name):
        method_frame, header_frame, body = self.channels[vhost].basic_get(queue=queue_name)
        try:
            data = json.loads(body)
        except ValueError, ex:
            data = body
        message = {'frame': method_frame,
                   'headers': header_frame.headers,
                   'body': data,
        }
        self.channels[vhost].basic_ack(method_frame.delivery_tag)
        return message

    def simulate_aleph_search_response(self, message, isbn):
        data = message['body']
        headers = message['headers']
        response = json.loads(open("resources/aleph-search-response.json").read())

        for record in response['records']:
            record['epublication']['ISBN'] = [isbn,]

        self.channels['aleph'].basic_publish(exchange='search',      
                                             routing_key='result',  
                                             body=json.dumps(response),
                                             properties = pika.BasicProperties(content_type='application/json',
                                                                               delivery_mode=2,
                                                                               headers = headers,  
                                                                           ) 
                                         )

    def simulate_aleph_export_response(self, message, isbn):
        data = message['body']
        headers = message['headers']
        response = json.loads(open("resources/aleph-export-response.json").read())
        response['ISBN'] = isbn
        self.channels['aleph'].basic_publish(exchange='export',      
                                             routing_key='result',  
                                             body=json.dumps(response),
                                             properties = pika.BasicProperties(content_type='application/json',
                                                                               delivery_mode=2,
                                                                               headers = headers,  
                                                                           ) 
                                         )


    def simulate_antivirus_response(self, message, fileName):
        data = message['body']
        headers = message['headers']
        response = json.loads(open("resources/antivirus-response.json").read())
        response['filename'] = fileName
        self.channels['antivirus'].basic_publish(exchange='antivirus',      
                                                 routing_key='result',
                                                 body=json.dumps(response),
                                                 properties = pika.BasicProperties(content_type='application/json',
                                                                                   delivery_mode=2,
                                                                                   headers = headers,  
                                                                               )
                                             )
        pass


    def simulate_isbn_validate_response(self, message, isbn, is_valid):
        data = message['body']
        headers = message['headers']
        response = json.loads(open("resources/isbn-validate-response.json").read())
        response['is_valid'] = bool(is_valid)
        self.channels['aleph'].basic_publish(exchange='validate',      
                                             routing_key='result',
                                             body=json.dumps(response),
                                             properties = pika.BasicProperties(content_type='application/json',
                                                                               delivery_mode=2,
                                                                               headers = headers,  
                                                                           )
                                         )
        pass

    def simulate_isbn_count_response(self, message, isbn, num_of_records):
        data = message['body']
        headers = message['headers']
        response = json.loads(open("resources/aleph-count-response.json").read())
        response['num_of_records'] = num_of_records
        self.channels['aleph'].basic_publish(exchange='count',      
                                             routing_key='result',
                                             body=json.dumps(response),
                                             properties = pika.BasicProperties(content_type='application/json',
                                                                               delivery_mode=2,
                                                                               headers = headers,  
                                                                           )
                                         )
        pass


    def simulate_aleph_export_exception(self, message):
        data = message['body']
        actual_headers = message['headers']
        #response = json.loads(open("resources/aleph-export-exception.json").read())
        #headers = dict(response['headers'],**actual_headers)
        headers = {
            "exception_type": "<class 'edeposit.amqp.aleph.export.ExportRejectedException'>",
            "exception": "Export request was rejected by import webform: Error - neplatne ISBN / ISMN",
            "exception_name": "ExportRejectedException",
            'traceback':"""Traceback (most recent call last):
File "/usr/lib/python2.7/site-packages/edeposit/amqp/amqpdaemon.py", line 141, in onMessageReceived
uuid
File "/usr/lib/python2.7/site-packages/edeposit/amqp/aleph/__init__.py", line 457, in reactToAMQPMessage
ISBN = ISBN.ISBN
File "/usr/lib/python2.7/site-packages/edeposit/amqp/aleph/export.py", line 379, in exportEPublication
return _sendPostDict(post_dict)
File "/usr/lib/python2.7/site-packages/edeposit/amqp/aleph/export.py", line 317, in _sendPostDict
headers["aleph-info"]
ExportRejectedException: Export request was rejected by import webform: Error - neplatne ISBN / ISMN""",
            'UUID': actual_headers['UUID']
        }

        self.channels['aleph'].basic_publish(exchange='export',
                                             routing_key='result',
                                             body="Export request was rejected by import webform: Error - neplatne ISBN / ISMN",
                                             properties = pika.BasicProperties(content_type='application/text',
                                                                               delivery_mode=2,
                                                                               headers = headers,  
                                                                           )
                                         )

        
    def get_num_of_messages_at_queue(self, vhost, queue_name):
        queue_info =  self.client.get_queue(vhost, queue_name)
        return queue_info['messages_ready']

    def delete_all_test_queues_starting_with(self, prefix):
        for vhost in self.connections.keys():
            testQueues = filter(lambda qq: qq['name'].startswith(prefix), self.client.get_queues(vhost))
            for queue in testQueues:
                qname = queue['name']
                print "detete queue %s/%s" % (vhost, qname)
                self.client.delete_queue(vhost,qname)

    def write_msg_into_file(self, msg, filename):
        open(filename,"wb").write(json.dumps({'body': msg['body'],
                                              'headers': msg['headers']
                                          }))
        pass

    def get_amqp_connections(self):
        import sys,pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        conn=self.client.get_connections()[0]
        conn['vhost']
        self.client.get_connections()
        pass
