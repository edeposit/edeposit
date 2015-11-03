E-Deposit
=========

Installation
------------


Install virtualenv for Python 2.7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	root@jan-XPS-L421X:~# aptitude install python-virtualenv 
	root@jan-XPS-L421X:~# aptitude install python-dev
        root@jan-XPS-L421X:~# aptitude install libjpeg-dev libfreetype6-dev
	root@jan-XPS-L421X:~# python --version
	Python 2.7.4

Prepare buildout for E-Deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:~# cd /opt
	jan@jan-XPS-L421X:~# git clone https://github.com/jstavel/edeposit.git edeposit
	jan@jan-XPS-L421X:~# cd /opt/edeposit
	jan@jan-XPS-L421X:/opt/edeposit# virtualenv .


Add optimistic transaction at code Product.CMFEdition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is due to plone.app.versioningbehavior.

CopyModifyMergeRepositoryTool.py

- set optimistic to True

::

        def _retrieve(...
            ...
            saved = transaction.savepoint(optimistic=True)
            ...
   

Doplnit savepoint pro typ Message pro zamqp modul
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
viz https://github.com/edeposit/edeposit/issues/532#issuecomment-135751913

hack, co vyradi NoRollbackSavepoints:

CopyModifyMergeRepositoryTool.py(498)

::

    _savepoints = filter(lambda ss: not isinstance(ss,transaction._transaction.NoRollbackSavepoint), saved._savepoints)
    saved._savepoints = _savepoints
    
Clone packages for E-Deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:/opt/edeposit$ mkdir src
	jan@jan-XPS-L421X:/opt/edeposit$ cd src
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.policy.git
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.content.git
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.user.git
	
Buildout of E-Deposit
~~~~~~~~~~~~~~~~~~~~~

::
	jan@jan-XPS-L421X:/opt/edeposit$ wget http://downloads.buildout.org/1/bootstrap.py
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/python bootstrap.py 
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/buildout 


Some extra work for edeposit.amq.storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This package uses newer version of ZODB. So it is imposible to install it by buildout.
The package should be installed by pip but without dependecies:

::
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/pip install -U --no-deps edeposit.amqp.storage

   
Installation of RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~~~

::
        root@jan-XPS-L421X:~# aptitude install erlang 
        

download release from http://www.rabbitmq.com/download.html
        
install rabbimq-server (latest version)
        
  
- add running server into supervisord configuration (in buildout deployment.cfg)
        store configuration files:

              buildout.d/rabbitmq/enabled_plugins
              buildout.d/rabbitmq/rabbitmq.config

into: /etc/rabbitmq
        
        - run rabbitmq
        - login into web: http://localhost:15672::
        
          | user     | quest |
          | password | quest |

- load configuration for file:
          
                buildout.d/rabbitmq/rabbitmq_edeposit.json

Producents and consuments will create its own bindings and queues.
That's it!                

Fonts configuration for AMQP PDFGen
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

see http://edeposit-amqp-pdfgen.readthedocs.org/en/latest/#open-suse

Module for LTP
~~~~~~~~~~~~~~

Module `edeposit.amqp.ltp` must be installed outside of buildout environment::

	edeposit-aplikace:/opt/edeposit # pip install -U edeposit.amqp.ltp
	
It is due to dependency on another version of ZODB than Plone application.


Create necessary folders in an application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Log in an application as admin.

Create somewhere:
- AMQP Classification Folder
- AMQP Tasks Folder

No mather as you name it.

Train AMQP Error Classificator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- upload corpus for NTLK::

   edeposit@edeposit-aplikace:~> ./bin/pip install textblob
   edeposit@edeposit-aplikace:~> ./bin/python -m textblob.download_corpora


- go to AMQP Classification Folder
- click action ``Train Classificator``
- upload csv with train data
