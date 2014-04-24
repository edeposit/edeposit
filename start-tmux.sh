#!/bin/bash
cd /opt/edeposit
./bin/supervisord

tmux new-session -d -s edeposit
 
tmux new-window     -t edeposit:1    -n 'supervisord'
tmux split-window   -t edeposit:1    -h -h 'watch ./bin/supervisorctl status'
tmux rotate-window  -t edeposit:1
tmux new-window     -t edeposit:2    -n 'varnish histogram' 'varnishhist'
tmux new-window     -t edeposit:3    -n 'edeposit' 'sudo su - edeposit'
tmux new-window     -t edeposit:4    -n 'alephdaemon' '/usr/bin/python2.7 /usr/lib/python2.7/site-packages/edeposit/amqp/alephdaemon.py start'

tmux ls | logger

exit
