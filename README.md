E-Deposit
=========

Installation
------------


Install virtualenv for Python 2.7
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	root@jan-XPS-L421X:~# aptitude install python-virtualenv 
	root@jan-XPS-L421X:~# aptitude install python-dev
	root@jan-XPS-L421X:~# python --version
	Python 2.7.4

Prepare buildout for E-Deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:~# cd /opt
	jan@jan-XPS-L421X:~# git clone https://github.com/jstavel/edeposit.git edeposit
	jan@jan-XPS-L421X:~# cd /opt/edeposit
	jan@jan-XPS-L421X:/opt/edeposit# virtualenv .
	jan@jan-XPS-L421X:/opt/edeposit# wget http://effbot.org/downloads/Imaging-1.1.7.tar.gz
	jan@jan-XPS-L421X:/opt/edeposit$ tar xfvz Imaging-1.1.7.tar.gz 
	jan@jan-XPS-L421X:/opt/edeposit$ cd Imaging-1.1.7/
	jan@jan-XPS-L421X:/opt/edeposit/Imaging-1.1.7$ ../bin/python setup.py install
	jan@jan-XPS-L421X:/opt/edeposit$ cd ..
	jan@jan-XPS-L421X:/opt/edeposit$ rm Imaging-1.1.7* -rf


Clone packages for E-Deposit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:/opt/edeposit$ cd src
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.policy.git
	jan@jan-XPS-L421X:/opt/edeposit/src$ git clone https://github.com/jstavel/edeposit.content.git
	
Buildout of E-Deposit
~~~~~~~~~~~~~~~~~~~~~

	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/python bootstrap.py 
	jan@jan-XPS-L421X:/opt/edeposit$ ./bin/buildout 
