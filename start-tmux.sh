#!/bin/bash
/etc/init.d/varnish start

cd /opt/edeposit
./bin/supervisord

tmux new-session -d -s edeposit
 
tmux new-window     -t edeposit:1    -n 'supervisord'
tmux split-window   -t edeposit:1    -h -h 'watch ./bin/supervisorctl status'
tmux rotate-window  -t edeposit:1
tmux new-window     -t edeposit:2    -n 'varnish histogram' 'varnishhist'
tmux new-window     -t edeposit:3    -n 'edeposit' 'sudo su - edeposit'

tmux ls | logger

exit
<<<<<<< HEAD

=======
>>>>>>> 1946e0fdeedf6077a86eea67d24e9052f24c8b96
