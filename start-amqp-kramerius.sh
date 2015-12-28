#!/bin/bash
cd /opt/edeposit/src/edeposit.amqp.kramerius
exec java -jar /opt/edeposit/src/edeposit.amqp.kramerius/target/edeposit.amqp.kramerius-1.0.3-standalone.jar --amqp
