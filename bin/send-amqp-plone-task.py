#!/usr/bin/python

import pika
import argparse
import json
import sys
import os.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from local_utils import updateMsg
except:
    updateMsg = lambda msg: msg

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send message to RabbitMQ to start some edeposit action")
    parser.add_argument('--file','-f', help="file with message to send", required=True)
    pargs = parser.parse_args()
    msg = updateMsg(json.loads(open(pargs.file,'rb').read()))
    conn = pika.BlockingConnection(pika.URLParameters("http://guest:guest@localhost:5672/plone"))
    channel = conn.channel()
    channel.basic_publish("task", "execute", json.dumps(msg), pika.BasicProperties(content_type="application/json",
                                                                       delivery_mode=2))
                                                                       
