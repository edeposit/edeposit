#!/bin/bash
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-declaration-with-error.json
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-file-problem.json
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-wrong-isbn-error.json
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-only-czech-isbn-accepted.json
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-isbn-already-exists-error.json
/opt/edeposit/bin/send-amqp-plone-task.py --file /opt/edeposit/docs/tests/resources/amqp/emails-to-all-producents-with-epublications-in-datum-vydani-is-required-error.json
