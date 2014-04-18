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


Clone packages for E-Deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:/opt/edeposit$ mkdir src
	jan@jan-XPS-L421X:/opt/edeposit$ cd src
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.policy.git
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.content.git
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.user.git
	
Buildout of E-Deposit
~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:/opt/edeposit$ wget http://downloads.buildout.org/1/bootstrap.py
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/python bootstrap.py 
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/buildout 


Installation of RabbitMQ
~~~~~~~~~~~~~~~~~~~~~~~~

        root@jan-XPS-L421X:~# aptitude install erlang 
        
        download release from http://www.rabbitmq.com/download.html
        
        install rabbimq-server (latest version)
        
        - add running server into supervisord configuration (in buildout deployment.cfg)
        store configuration files:

              buildout.d/rabbitmq/enabled_plugins
              buildout.d/rabbitmq/rabbitmq.config

        into: /etc/rabbitmq
        
        - run rabbitmq
        - login into web: http://localhost:15672

          | user     | quest |
          | password | quest |

        - load configuration for file:
          
                buildout.d/rabbitmq/rabbitmq_edeposit.json

        Producents and consuments will create its own bindings and queues.
        That's it!                
