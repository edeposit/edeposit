#!/usr/bin/python

import pika
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send message to RabbitMQ to start some edeposit action")
    parser.add_argument('--file','-f', help="file with message to send", required=True)
    pargs = parser.parse_args()
    msg = open(pargs.file,'rb').read()
    conn = pika.BlockingConnection(pika.URLParameters("http://guest:guest@localhost:5672/plone"))
    channel = conn.channel()
    channel.basic_publish("task", "execute", msg, pika.BasicProperties(content_type="application/json",
                                                                       delivery_mode=2))
                                                                       
