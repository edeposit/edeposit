#!/bin/bash
# . /opt/edeposit/etc/periodic-jobs.sh
# LINK="${URL}/${WORKFLOW_ACTION}=sendEmailToISBNGeneration"
# echo $LINK
# curl -u ${USER}:${PASSWORD} $LINK
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/email-for-isbn-generation.json
