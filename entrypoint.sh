#!/bin/bash

printenv | sed 's/^\(.*\)$/export \1/g' | grep -E "^export HTUPD"  > /etc/environment
source /etc/environment

cron -f
