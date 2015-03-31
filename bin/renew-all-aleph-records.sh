#!/bin/bash
# . /opt/edeposit/etc/periodic-jobs.sh
# LINK="${URL}/content_status_modify?workflow_action=renewAlephRecords"
# echo $LINK
# curl -u ${USER}:${PASSWORD} $LINK
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/renew-aleph-records.json
