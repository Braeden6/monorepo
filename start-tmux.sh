#!/bin/bash

MONOREPO_ROOT=/Users/braeden/Documents/code/personal/monorepo
API_ROOT=/Users/braeden/Documents/code/personal/monorepo/services/recipe-api

tmux kill-session -t personal 2>/dev/null

tmux new-session -d -s personal -n api -c $API_ROOT

# Window 1: api 
tmux split-window -h -t personal:1 -c $API_ROOT

tmux send-keys -t personal:1.0 'uv run src/recipe_api/main.py' C-m

# Window 2: frontend
tmux new-window -t personal:2 -n frontend -c $MONOREPO_ROOT
tmux split-window -h -t personal:2.0 -c $MONOREPO_ROOT

tmux send-keys -t personal:2.0 'pnpm dev' C-m

# Window 3: k9s
tmux new-window -t personal:3 -n k9s -c $MONOREPO_ROOT

tmux send-key -t personal:3.0 'k9s' C-m




tmux select-window -t personal:1
tmux attach-session -t personal