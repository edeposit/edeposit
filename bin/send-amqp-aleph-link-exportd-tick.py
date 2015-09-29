#!/usr/bin/python

import pika
import argparse
import datetime
from edeposit.amqp.aleph_link_export import StatusRequest
from edeposit.amqp.serializers import serialize

"""
(project-shell "*shell*" "/usr/bin")
(project-task send-amqp-aleph-link-exportd "*shell*" "send-amqp-aleph-link-exportd-tick.py")

(local-set-key (kbd "C-c C-c") 'send-amqp-aleph-link-exportd)
(local-set-key (kbd "C-c l") 'send-current-line-to-shell)
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send message to RabbitMQ to update status at Aleph Link Exportd")
    pargs = parser.parse_args()
    conn = pika.BlockingConnection(pika.URLParameters("http://guest:guest@localhost:5672/aleph"))
    channel = conn.channel()
    request=StatusRequest()
    channel.basic_publish("update-links", "tick", serialize(request), 
                          pika.BasicProperties(content_type="application/json",
                                               headers=dict(UUID=str(datetime.datetime.now())),
                                               delivery_mode=2))
