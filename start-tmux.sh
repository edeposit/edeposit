#!/bin/bash
tmux new-session -d -s edeposit
 
tmux new-window     -t edeposit:1    -n 'supervisor'
tmux split-window   -t edeposit:1    -h -h 'watch supervisorctl status'
tmux rotate-window  -t edeposit:1
tmux new-window     -t edeposit:2    -n 'varnish histogram' 'varnishhist'
tmux new-window     -t edeposit:3    -n 'edeposit' 'sudo su - edeposit'

tmux ls | logger

exit
