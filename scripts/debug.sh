#!/bin/sh

tmux \
	new-session 'sh -c "echo \"Running local api and frontend\"; read -p \"Press any key to exit...\"; tmux kill-session"' \; \
	split-window -v -p 90 'sh -c "make -C api debug; read -p \"Exited with code $?\""' \; \
	split-window -h 'sh -c "make -C frontend debug; read -p \"Exited with code $?\""' \; \
	select-pane -t 0 \;
