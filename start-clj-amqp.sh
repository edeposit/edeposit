#!/bin/bash
cd /opt/edeposit/src/edeposit.clj-amqp
exec java -jar /opt/edeposit/src/edeposit.clj-amqp/target/edeposit.clj-amqp-1.0.1-standalone.jar --amqp
