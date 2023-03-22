#!/bin/bash

# This script will navigate to every directory in the current folder
# and execute "git checkout 15.0" and "git pull" commands.

for dir in */ ; do
  cd "$dir"
  echo "Entering directory: $(pwd)"
  git checkout 15.0
  git pull
  cd ..
done