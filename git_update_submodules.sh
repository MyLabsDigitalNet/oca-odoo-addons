#!/bin/bash

# This script will navigate to every directory in the current folder
# and execute "git checkout 16.0" and "git pull" commands.

# For use only in main repository not in submodules.

for dir in */ ; do
  cd "$dir"
  echo "Entering directory: $(pwd)"
  git checkout 16.0
  git pull
  cd ..
done