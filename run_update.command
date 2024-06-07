#!/bin/bash

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

cd $SCRIPT_DIR
poetry run python3 update_indexes.py

git pull
git add .
git commit -m "bump"
git add .
git commit -m "bump"

git push origin main
