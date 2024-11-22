#!/bin/bash

cd $HOME/src
git pull origin main
git add -A
git commit -m "Auto-sync: $(date)"
git push origin main
