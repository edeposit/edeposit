#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# library for Robot Framework to work with RabbitMQ
#

import pika
import json

class RabbitMQ(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost',
            virtual_host="aleph",
        ))
        self.channel = self.connection.channel()

    def declare_queue(self,queue_name, durable=False):
        self.channel.queue_declare(queue=queue_name, durable=durable)        

    def delete_queue(self, queue_name):
        self.channel.queue_delete(queue=queue_name)
        
    def declare_queue_binding(self, exchange_name, queue_name,  routing_key):
        self.channel.queue_bind( 
            exchange = str(exchange_name),
            queue = str(queue_name),
            routing_key = str(routing_key)
        )
        
    def get_message_from_queue(self, queue_name):
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name)
        try:
            data = json.loads(body)
        except ValueError, ex:
            data = body
        message = {'frame': method_frame,
                   'headers': header_frame.headers,
                   'body': data,
        }
        self.channel.basic_ack(method_frame.delivery_tag)
        return message

    def close_connection(self):
        self.connection.close()
        
