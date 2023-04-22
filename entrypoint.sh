#!/bin/bash

printenv | sed 's/^\(.*\)$/export \1/g' | grep -E "^export HTUPD"  >> /etc/environment

/usr/bin/python3 /app/app.py