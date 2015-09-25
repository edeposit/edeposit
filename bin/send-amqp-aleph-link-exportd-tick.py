#!/usr/bin/python

import pika
import argparse
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send message to RabbitMQ to update status at Aleph Link Exportd")
    pargs = parser.parse_args()
    conn = pika.BlockingConnection(pika.URLParameters("http://guest:guest@localhost:5672/aleph"))
    channel = conn.channel()
    channel.basic_publish("update-links", "tick", "1", pika.BasicProperties(content_type="application/json",
                                                                            headers=dict(UUID=str(datetime.datetime.now())),
                                                                            delivery_mode=2))
                                                                       
